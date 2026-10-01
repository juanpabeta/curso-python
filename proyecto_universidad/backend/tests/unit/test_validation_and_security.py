"""Pruebas unitarias: lógica pura, sin base de datos ni red."""

from datetime import date, timedelta

import pytest
from jose import jwt
from pydantic import ValidationError

from app.auth.schemas import LoginRequest
from app.core.config import Settings
from app.core.exceptions import UnauthorizedError
from app.core.security import create_access_token, decode_access_token
from app.enrollments.schemas import (
    AcademicPeriodCreate,
    EnrollmentCreate,
    EnrollmentUpdate,
)
from app.grades.schemas import GradeCreate, GradeUpdate
from app.subjects.schemas import SubjectCreate, SubjectUpdate
from app.users.models import User
from app.users.schemas import RoleCreate, RoleUpdate, UserCreate, UserUpdate

pytestmark = pytest.mark.unit


@pytest.mark.parametrize(
    ("email", "expected"),
    [
        ("STUDENT@UNIVERSIDAD.TEST", "student@universidad.test"),
        ("ana.lopez+qa@universidad.edu", "ana.lopez+qa@universidad.edu"),
    ],
)
def test_user_create_normalizes_valid_email(email: str, expected: str) -> None:
    # Arrange / Act
    user = UserCreate(email=email, full_name="Ana López", password="SecurePass123!")

    # Assert
    assert user.email == expected


@pytest.mark.parametrize(
    "email",
    ["", "sin-arroba.test", "@universidad.test", "user@localhost", "a b@universidad.test"],
)
def test_user_create_rejects_invalid_email(email: str) -> None:
    with pytest.raises(ValidationError):
        UserCreate(email=email, full_name="Ana López", password="SecurePass123!")


@pytest.mark.parametrize("credits", [1, 12])
def test_subject_accepts_credit_boundaries(credits: int) -> None:
    subject = SubjectCreate(code="QA101", name="Testing", credits=credits)
    assert subject.credits == credits


@pytest.mark.parametrize("credits", [0, -1, 13, None, "muchos"])
def test_subject_rejects_invalid_credits(credits) -> None:
    with pytest.raises(ValidationError):
        SubjectCreate(code="QA101", name="Testing", credits=credits)


@pytest.mark.parametrize("score", [0, 50.5, 100])
def test_grade_accepts_score_boundaries(score: float) -> None:
    grade = GradeCreate(enrollment_id=1, type="Final", score=score)
    assert grade.score == score


@pytest.mark.parametrize("score", [-0.1, 100.1, None, "alto"])
def test_grade_rejects_out_of_range_or_wrong_type(score) -> None:
    with pytest.raises(ValidationError):
        GradeCreate(enrollment_id=1, type="Final", score=score)


def test_login_rejects_surrounding_spaces_as_tampered_input() -> None:
    with pytest.raises(ValidationError):
        LoginRequest(email=" admin@universidad.test ", password="Secret123!")


def test_user_model_normalizes_email() -> None:
    user = User(
        email="  ADMIN@UNIVERSIDAD.TEST ",
        full_name="Admin",
        password_hash="not-used",
    )
    assert user.email == "admin@universidad.test"


def test_token_round_trip_preserves_subject_and_roles() -> None:
    token = create_access_token("42", roles=["Estudiante"], expires_minutes=5)
    payload = decode_access_token(token)
    assert payload["sub"] == "42"
    assert payload["roles"] == ["Estudiante"]


def test_decode_rejects_tampered_token() -> None:
    with pytest.raises(UnauthorizedError, match="Token inválido"):
        decode_access_token("header.payload.signature-manipulada")


def test_decode_rejects_expired_token() -> None:
    token = create_access_token("42", expires_minutes=-1)
    with pytest.raises(UnauthorizedError):
        decode_access_token(token)


def test_settings_parse_csv_and_detect_production(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENV", "production")
    settings = Settings(
        app_cors_origins="https://a.test, https://b.test,",
        _env_file=None,
    )
    assert settings.is_production is True
    assert settings.app_cors_origins == ["https://a.test", "https://b.test"]


def test_token_with_explicit_expiration_is_signed() -> None:
    token = create_access_token("7", expires_minutes=int(timedelta(minutes=1).total_seconds() / 60))
    assert len(jwt.get_unverified_claims(token)["sub"]) == 1


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("full_name", "A"),
        ("full_name", "A" * 201),
        ("password", "short"),
        ("password", "x" * 129),
    ],
)
def test_user_create_rejects_invalid_text_boundaries(field: str, value: str) -> None:
    payload = {
        "email": "student@universidad.test",
        "full_name": "Estudiante Prueba",
        "password": "SecurePass123!",
        field: value,
    }

    with pytest.raises(ValidationError):
        UserCreate(**payload)


def test_user_update_normalizes_email_and_accepts_partial_payload() -> None:
    update = UserUpdate(email="  NEW@UNIVERSIDAD.TEST  ")

    assert update.email == "new@universidad.test"
    assert update.full_name is None
    assert update.password is None


@pytest.mark.parametrize("email", ["bad", "@domain.test", "user@localhost", "a b@domain.test"])
def test_user_update_rejects_invalid_email(email: str) -> None:
    with pytest.raises(ValidationError):
        UserUpdate(email=email)


@pytest.mark.parametrize(
    ("schema", "payload"),
    [
        (RoleCreate, {"name": "A"}),
        (RoleCreate, {"name": "R" * 51}),
        (RoleUpdate, {"description": "D" * 256}),
        (SubjectUpdate, {"code": "X"}),
        (SubjectUpdate, {"description": "D" * 501}),
        (EnrollmentUpdate, {"status": "x"}),
        (GradeUpdate, {"type": "x"}),
        (GradeUpdate, {"comments": "C" * 501}),
    ],
)
def test_update_and_role_schemas_reject_invalid_lengths(schema, payload: dict) -> None:
    with pytest.raises(ValidationError):
        schema(**payload)


def test_academic_period_parses_iso_dates_deterministically() -> None:
    period = AcademicPeriodCreate(
        code="2026-1",
        name="Primer semestre",
        start_date="2026-01-15",
        end_date="2026-06-15",
    )

    assert period.start_date == date(2026, 1, 15)
    assert period.end_date == date(2026, 6, 15)


@pytest.mark.parametrize(
    "payload",
    [
        {"code": "", "name": "Periodo", "start_date": "2026-01-01", "end_date": "2026-06-01"},
        {"code": "2026-1", "name": "", "start_date": "2026-01-01", "end_date": "2026-06-01"},
        {"code": "2026-1", "name": "Periodo", "start_date": "no-date", "end_date": "2026-06-01"},
        {"code": "2026-1", "name": "Periodo", "start_date": None, "end_date": "2026-06-01"},
    ],
)
def test_academic_period_rejects_invalid_required_values(payload: dict) -> None:
    with pytest.raises(ValidationError):
        AcademicPeriodCreate(**payload)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("user_id", None),
        ("subject_id", "abc"),
        ("period_id", 1.5),
        ("status", ""),
        ("status", "x" * 21),
    ],
)
def test_enrollment_rejects_null_wrong_type_and_invalid_status(
    field: str,
    value,
) -> None:
    payload = {
        "user_id": 1,
        "subject_id": 2,
        "period_id": 3,
        "status": "active",
        field: value,
    }

    with pytest.raises(ValidationError):
        EnrollmentCreate(**payload)
