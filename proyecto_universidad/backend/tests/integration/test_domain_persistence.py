"""Integración de servicios de dominio con SQLite y relaciones reales."""

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import DuplicateError, NotFoundError
from app.core.security import verify_password
from app.enrollments.models import AcademicPeriod, Enrollment
from app.enrollments.schemas import AcademicPeriodCreate, AcademicPeriodUpdate
from app.enrollments.services import AcademicPeriodService
from app.grades.models import Grade
from app.grades.schemas import GradeCreate, GradeUpdate
from app.grades.services import GradeService
from app.users.models import Role, User, UserRole
from app.users.schemas import RoleCreate, UserCreate, UserUpdate
from app.users.services import RoleService, UserService

pytestmark = pytest.mark.integration


def test_user_crud_hashes_password_and_persists_partial_update(
    db_session: Session,
) -> None:
    # Arrange
    service = UserService(db_session)
    payload = UserCreate(
        email="learner@universidad.test",
        full_name="Estudiante Inicial",
        password="InitialPass123!",
    )

    # Act
    created = service.create(payload)
    updated = service.update(
        created.id,
        UserUpdate(full_name="Estudiante Actualizado", password="ChangedPass123!"),
    )

    # Assert
    assert created.password_hash != payload.password
    assert verify_password("ChangedPass123!", updated.password_hash)
    assert updated.email == payload.email
    assert updated.full_name == "Estudiante Actualizado"
    assert service.get_all() == [created]

    service.delete(created.id)
    with pytest.raises(NotFoundError):
        service.get_by_id(created.id)


def test_user_service_rejects_duplicate_normalized_email(
    db_session: Session,
) -> None:
    service = UserService(db_session)
    service.create(
        UserCreate(
            email="duplicate@universidad.test",
            full_name="Primero",
            password="SecurePass123!",
        ),
    )

    with pytest.raises(DuplicateError, match="email"):
        service.create(
            UserCreate(
                email=" DUPLICATE@UNIVERSIDAD.TEST ",
                full_name="Segundo",
                password="SecurePass123!",
            ),
        )


def test_role_crud_and_assignment_persist_many_to_many_relation(
    db_session: Session,
    admin_user: User,
) -> None:
    service = RoleService(db_session)
    role = service.create(RoleCreate(name="Auditor", description="Solo lectura"))

    relation = service.assign_role_to_user(admin_user.id, role.id)

    assert relation.user_id == admin_user.id
    assert db_session.scalar(select(UserRole).where(UserRole.id == relation.id)) is relation
    db_session.refresh(admin_user)
    assert "Auditor" in admin_user.role_names

    with pytest.raises(DuplicateError, match="ya tiene"):
        service.assign_role_to_user(admin_user.id, role.id)

    service.delete(role.id)
    assert db_session.get(Role, role.id) is None


@pytest.mark.parametrize(
    ("user_id", "role_id", "missing_entity"),
    [(999, 1, "Usuario"), (1, 999, "Rol")],
)
def test_role_assignment_rejects_missing_foreign_entity(
    db_session: Session,
    admin_user: User,
    user_id: int,
    role_id: int,
    missing_entity: str,
) -> None:
    existing_role = admin_user.roles[0]
    actual_user_id = admin_user.id if user_id == 1 else user_id
    actual_role_id = existing_role.id if role_id == 1 else role_id

    with pytest.raises(NotFoundError, match=missing_entity):
        RoleService(db_session).assign_role_to_user(actual_user_id, actual_role_id)


def test_academic_period_crud_and_duplicate_code(
    db_session: Session,
) -> None:
    service = AcademicPeriodService(db_session)
    payload = AcademicPeriodCreate(
        code="2027-1",
        name="Primer semestre 2027",
        start_date="2027-01-15",
        end_date="2027-06-15",
    )

    created = service.create(payload)
    updated = service.update(
        created.id,
        AcademicPeriodUpdate(name="Semestre actualizado", end_date="2027-06-30"),
    )

    assert updated.name == "Semestre actualizado"
    assert str(updated.end_date) == "2027-06-30"
    assert service.get_all() == [created]
    with pytest.raises(DuplicateError, match="código"):
        service.create(payload)

    service.delete(created.id)
    assert db_session.get(AcademicPeriod, created.id) is None


def test_grade_crud_persists_enrollment_relationship(
    db_session: Session,
    enrollment: Enrollment,
) -> None:
    service = GradeService(db_session)
    created = service.create(
        GradeCreate(
            enrollment_id=enrollment.id,
            type="Parcial",
            score=75,
            comments=None,
        ),
    )

    updated = service.update(
        created.id,
        GradeUpdate(type="Final", score=92.5, comments="Aprobado"),
    )

    assert updated.enrollment is enrollment
    assert updated.type == "Final"
    assert updated.score == 92.5
    assert service.get_all() == [created]

    service.delete(created.id)
    with pytest.raises(NotFoundError):
        service.get_by_id(created.id)


def test_grade_rejects_missing_enrollment_at_service_boundary(
    db_session: Session,
) -> None:
    with pytest.raises(NotFoundError, match="Inscripción"):
        GradeService(db_session).create(
            GradeCreate(enrollment_id=999, type="Final", score=80),
        )


def test_database_enforces_grade_foreign_key(db_session: Session) -> None:
    db_session.add(
        Grade(enrollment_id=999, type="Final", score=80, comments=None),
    )

    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_database_fixture_starts_without_shared_domain_state(
    db_session: Session,
) -> None:
    assert db_session.scalars(select(User)).all() == []
    assert db_session.scalars(select(Enrollment)).all() == []
