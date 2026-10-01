"""Uso pedagógico de Mock y monkeypatch sobre dependencias externas."""

from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from app.auth.schemas import LoginRequest
from app.auth.services import AuthService
from app.core.exceptions import DuplicateError, NotFoundError, UnauthorizedError
from app.enrollments.schemas import AcademicPeriodCreate, EnrollmentUpdate
from app.enrollments.services import AcademicPeriodService, EnrollmentService
from app.grades.schemas import GradeCreate
from app.grades.services import GradeService
from app.subjects.schemas import SubjectCreate
from app.subjects.services import SubjectService
from app.users.schemas import RoleCreate, UserCreate, UserUpdate
from app.users.services import RoleService, UserService

pytestmark = pytest.mark.unit


def _execute_result(value) -> MagicMock:
    result = MagicMock()
    result.scalar_one_or_none.return_value = value
    return result


def test_user_service_create_hashes_password_and_commits(monkeypatch: pytest.MonkeyPatch) -> None:
    # Arrange
    db = MagicMock()
    db.execute.return_value = _execute_result(None)
    monkeypatch.setattr("app.users.services.hash_password", lambda value: f"hash::{value}")
    payload = UserCreate(
        email="new@universidad.test",
        full_name="Usuario Nuevo",
        password="Secret123!",
    )

    # Act
    created = UserService(db).create(payload)

    # Assert
    assert created.password_hash == "hash::Secret123!"
    db.add.assert_called_once_with(created)
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(created)


def test_user_service_rejects_duplicate_without_writing() -> None:
    db = MagicMock()
    db.execute.return_value = _execute_result(SimpleNamespace(id=1))

    with pytest.raises(DuplicateError, match="email"):
        UserService(db).create(
            UserCreate(
                email="duplicate@universidad.test",
                full_name="Duplicado",
                password="Secret123!",
            )
        )

    db.add.assert_not_called()
    db.commit.assert_not_called()


def test_subject_service_rejects_duplicate_code() -> None:
    db = MagicMock()
    db.execute.return_value = _execute_result(SimpleNamespace(id=1))
    payload = SubjectCreate(code="QA101", name="Testing", credits=3)

    with pytest.raises(DuplicateError, match="código"):
        SubjectService(db).create(payload)


def test_subject_service_get_missing_raises_domain_error() -> None:
    db = MagicMock()
    db.get.return_value = None
    with pytest.raises(NotFoundError, match="99"):
        SubjectService(db).get_by_id(99)


@pytest.mark.parametrize(
    ("user", "password_ok", "message"),
    [
        (None, True, "Credenciales inválidas"),
        (SimpleNamespace(password_hash="hash", is_active=True, roles=[]), False, "Credenciales inválidas"),
        (SimpleNamespace(password_hash="hash", is_active=False, roles=[]), True, "Usuario inactivo"),
    ],
)
def test_auth_service_rejects_invalid_login_states(
    monkeypatch: pytest.MonkeyPatch,
    user,
    password_ok: bool,
    message: str,
) -> None:
    db = MagicMock()
    db.execute.return_value = _execute_result(user)
    monkeypatch.setattr("app.auth.services.verify_password", lambda *_: password_ok)

    with pytest.raises(UnauthorizedError, match=message):
        AuthService(db).login(
            LoginRequest(email="user@universidad.test", password="Secret123!")
        )


def test_auth_service_issues_token_with_roles(monkeypatch: pytest.MonkeyPatch) -> None:
    user = SimpleNamespace(
        id=8,
        password_hash="hash",
        is_active=True,
        roles=[SimpleNamespace(name="Docente")],
    )
    db = MagicMock()
    db.execute.return_value = _execute_result(user)
    monkeypatch.setattr("app.auth.services.verify_password", lambda *_: True)
    issue_token = MagicMock(return_value="signed-token")
    monkeypatch.setattr("app.auth.services.create_access_token", issue_token)

    token = AuthService(db).login(
        LoginRequest(email="teacher@universidad.test", password="Secret123!")
    )

    assert token == "signed-token"
    issue_token.assert_called_once_with("8", roles=["Docente"])


def test_user_service_updates_only_supplied_fields(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    db = MagicMock()
    user = SimpleNamespace(
        email="old@universidad.test",
        full_name="Nombre Original",
        password_hash="old-hash",
        is_active=True,
        is_superuser=False,
    )
    db.get.return_value = user
    monkeypatch.setattr("app.users.services.hash_password", lambda value: f"hash::{value}")

    updated = UserService(db).update(
        1,
        UserUpdate(
            email="new@universidad.test",
            password="NewSecret123!",
            is_active=False,
            is_superuser=True,
        ),
    )

    assert updated.email == "new@universidad.test"
    assert updated.full_name == "Nombre Original"
    assert updated.password_hash == "hash::NewSecret123!"
    assert updated.is_active is False
    assert updated.is_superuser is True
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(user)


def test_user_service_delete_does_not_write_when_user_is_missing() -> None:
    db = MagicMock()
    db.get.return_value = None

    with pytest.raises(NotFoundError, match="Usuario"):
        UserService(db).delete(404)

    db.delete.assert_not_called()
    db.commit.assert_not_called()


def test_role_service_create_persists_new_role() -> None:
    db = MagicMock()
    db.execute.return_value = _execute_result(None)

    role = RoleService(db).create(
        RoleCreate(name="Auditor", description="Revisa operaciones"),
    )

    assert role.name == "Auditor"
    db.add.assert_called_once_with(role)
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(role)


def test_role_service_rejects_duplicate_name_without_writing() -> None:
    db = MagicMock()
    db.execute.return_value = _execute_result(SimpleNamespace(id=1))

    with pytest.raises(DuplicateError, match="rol"):
        RoleService(db).create(RoleCreate(name="Administrador"))

    db.add.assert_not_called()
    db.commit.assert_not_called()


@pytest.mark.parametrize(
    ("user", "role", "missing_entity"),
    [
        (None, SimpleNamespace(id=2), "Usuario"),
        (SimpleNamespace(id=1), None, "Rol"),
    ],
)
def test_assign_role_rejects_missing_entities(
    user,
    role,
    missing_entity: str,
) -> None:
    db = MagicMock()
    db.get.side_effect = [user, role]

    with pytest.raises(NotFoundError, match=missing_entity):
        RoleService(db).assign_role_to_user(1, 2)

    db.add.assert_not_called()
    db.commit.assert_not_called()


def test_assign_role_rejects_existing_relation() -> None:
    db = MagicMock()
    db.get.side_effect = [SimpleNamespace(id=1), SimpleNamespace(id=2)]
    db.execute.return_value = _execute_result(SimpleNamespace(id=3))

    with pytest.raises(DuplicateError, match="ya tiene"):
        RoleService(db).assign_role_to_user(1, 2)

    db.add.assert_not_called()
    db.commit.assert_not_called()


def test_period_service_create_commits_valid_period() -> None:
    db = MagicMock()
    db.execute.return_value = _execute_result(None)
    payload = AcademicPeriodCreate(
        code="2026-2",
        name="Segundo semestre",
        start_date="2026-07-01",
        end_date="2026-12-01",
    )

    period = AcademicPeriodService(db).create(payload)

    assert period.code == "2026-2"
    assert period.start_date == payload.start_date
    db.add.assert_called_once_with(period)
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(period)


def test_enrollment_service_partial_update_changes_only_status() -> None:
    db = MagicMock()
    enrollment = SimpleNamespace(
        user_id=1,
        subject_id=2,
        period_id=3,
        status="active",
    )
    db.get.return_value = enrollment

    updated = EnrollmentService(db).update(
        9,
        EnrollmentUpdate(status="completed"),
    )

    assert updated.status == "completed"
    assert (updated.user_id, updated.subject_id, updated.period_id) == (1, 2, 3)
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(enrollment)


def test_grade_service_rejects_missing_enrollment_without_writing() -> None:
    db = MagicMock()
    db.get.return_value = None

    with pytest.raises(NotFoundError, match="Inscripción"):
        GradeService(db).create(
            GradeCreate(enrollment_id=999, type="Final", score=85),
        )

    db.add.assert_not_called()
    db.commit.assert_not_called()


def test_grade_service_create_persists_grade() -> None:
    db = MagicMock()
    db.get.return_value = SimpleNamespace(id=4)

    grade = GradeService(db).create(
        GradeCreate(
            enrollment_id=4,
            type="Final",
            score=85,
            comments="Aprobado",
        ),
    )

    assert grade.enrollment_id == 4
    assert grade.score == 85
    db.add.assert_called_once_with(grade)
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(grade)
