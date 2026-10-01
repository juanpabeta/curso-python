"""Flujo de usuario completo disponible hoy, sin mocks internos."""

import pytest
from fastapi.testclient import TestClient

from tests.factories.domain import period_data, subject_data, user_data

pytestmark = pytest.mark.e2e


def test_admin_registers_student_and_completes_academic_flow(
    api_client: TestClient,
    admin_user,
) -> None:
    # Arrange: autenticación real contra el usuario persistido.
    login = api_client.post(
        "/auth/login",
        json={"email": admin_user.email, "password": "Secret123!"},
    )
    assert login.status_code == 200
    headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

    # Act: registro, curso, periodo, matrícula y calificación por HTTP.
    student = api_client.post("/users/", json=user_data(), headers=headers)
    subject = api_client.post("/subjects/", json=subject_data(), headers=headers)
    period = api_client.post("/periods/", json=period_data(), headers=headers)
    assert (student.status_code, subject.status_code, period.status_code) == (201, 201, 201)

    enrollment = api_client.post(
        "/enrollments/",
        json={
            "user_id": student.json()["id"],
            "subject_id": subject.json()["id"],
            "period_id": period.json()["id"],
            "status": "active",
        },
        headers=headers,
    )
    assert enrollment.status_code == 201

    grade = api_client.post(
        "/grades/",
        json={
            "enrollment_id": enrollment.json()["id"],
            "type": "Final",
            "score": 92.5,
            "comments": "Aprobado",
        },
        headers=headers,
    )

    # Assert: la consulta final refleja lo persistido.
    assert grade.status_code == 201
    assert grade.json()["score"] == 92.5
    assert api_client.get("/enrollments/", headers=headers).json() == [enrollment.json()]
    assert api_client.get("/grades/", headers=headers).json() == [grade.json()]


@pytest.mark.security
def test_inactive_user_cannot_login(api_client: TestClient, admin_user, db_session) -> None:
    admin_user.is_active = False
    db_session.commit()
    response = api_client.post(
        "/auth/login",
        json={"email": admin_user.email, "password": "Secret123!"},
    )
    assert response.status_code == 401
