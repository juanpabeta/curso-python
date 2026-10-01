"""Integración servicios + SQLAlchemy + SQLite real en memoria."""

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import DuplicateError, NotFoundError
from app.enrollments.schemas import EnrollmentCreate
from app.enrollments.services import EnrollmentService
from app.subjects.models import Subject
from app.subjects.schemas import SubjectCreate, SubjectUpdate
from app.subjects.services import SubjectService
from app.users.models import User

pytestmark = pytest.mark.integration


def test_subject_crud_is_persisted(db_session: Session) -> None:
    # Arrange
    service = SubjectService(db_session)

    # Act
    created = service.create(
        SubjectCreate(code="ARQ101", name="Arquitectura de software", credits=4)
    )
    updated = service.update(created.id, SubjectUpdate(credits=5))

    # Assert
    assert db_session.get(Subject, created.id).name == "Arquitectura de software"
    assert updated.credits == 5
    assert service.get_all() == [created]

    service.delete(created.id)
    with pytest.raises(NotFoundError):
        service.get_by_id(created.id)


def test_subject_duplicate_code_is_a_domain_conflict(db_session: Session) -> None:
    service = SubjectService(db_session)
    payload = SubjectCreate(code="DUP101", name="Original", credits=3)
    service.create(payload)
    with pytest.raises(DuplicateError):
        service.create(payload)


def test_database_enforces_unique_normalized_email(db_session: Session) -> None:
    first = User(email="same@universidad.test", full_name="Uno", password_hash="hash")
    second = User(email=" SAME@UNIVERSIDAD.TEST ", full_name="Dos", password_hash="hash")
    db_session.add_all([first, second])

    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_enrollment_persists_relationships_and_blocks_duplicate(
    db_session: Session,
    admin_user: User,
    course: Subject,
    academic_period,
) -> None:
    service = EnrollmentService(db_session)
    payload = EnrollmentCreate(
        user_id=admin_user.id,
        subject_id=course.id,
        period_id=academic_period.id,
        status="active",
    )

    created = service.create(payload)

    assert created.user.email == admin_user.email
    assert created.subject.code == course.code
    with pytest.raises(DuplicateError):
        service.create(payload)


@pytest.mark.parametrize(
    ("user_id", "subject_id", "period_id", "missing_entity"),
    [(999, 1, 1, "Usuario"), (1, 999, 1, "Materia"), (1, 1, 999, "Periodo")],
)
def test_enrollment_rejects_missing_foreign_entities(
    db_session: Session,
    admin_user: User,
    course: Subject,
    academic_period,
    user_id: int,
    subject_id: int,
    period_id: int,
    missing_entity: str,
) -> None:
    ids = {
        "user_id": admin_user.id if user_id == 1 else user_id,
        "subject_id": course.id if subject_id == 1 else subject_id,
        "period_id": academic_period.id if period_id == 1 else period_id,
    }
    with pytest.raises(NotFoundError, match=missing_entity):
        EnrollmentService(db_session).create(EnrollmentCreate(**ids))
