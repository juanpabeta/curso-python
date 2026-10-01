"""Recorrido E2E de administración, rol estudiante y expediente académico."""

import pytest
from fastapi.testclient import TestClient

from tests.factories.domain import (
    enrollment_data,
    grade_data,
    period_data,
    role_data,
    subject_data,
    user_data,
)

pytestmark = pytest.mark.e2e


def test_admin_onboards_student_then_student_completes_available_journey(
    api_client: TestClient,
    admin_user,
) -> None:
    # Arrange: el administrador inicia sesión y aprovisiona cuenta y rol.
    admin_login = api_client.post(
        "/auth/login",
        json={"email": admin_user.email, "password": "Secret123!"},
    )
    assert admin_login.status_code == 200

    student = api_client.post(
        "/users/",
        json=user_data(email="journey.student@universidad.test"),
    )
    role = api_client.post(
        "/roles/",
        json=role_data(name="Estudiante"),
    )
    assert (student.status_code, role.status_code) == (201, 201)
    assignment = api_client.post(
        f"/users/{student.json()['id']}/roles/{role.json()['id']}",
    )
    assert assignment.status_code == 201

    # Act: se cambia de sesión y el estudiante usa el flujo disponible.
    assert api_client.post("/auth/logout").status_code == 200
    student_login = api_client.post(
        "/auth/login",
        json={
            "email": student.json()["email"],
            "password": "SecurePass123!",
        },
    )
    assert student_login.status_code == 200

    own_profile = api_client.get(f"/users/{student.json()['id']}")
    forbidden_admin_list = api_client.get("/users/")
    subject = api_client.post(
        "/subjects/",
        json=subject_data(code="E2E201", name="Pruebas E2E"),
    )
    period = api_client.post(
        "/periods/",
        json=period_data(code="E2E-2026"),
    )
    enrollment = api_client.post(
        "/enrollments/",
        json=enrollment_data(
            student.json()["id"],
            subject.json()["id"],
            period.json()["id"],
        ),
    )
    grade = api_client.post(
        "/grades/",
        json=grade_data(enrollment.json()["id"], score=96.5),
    )

    # Assert: RBAC y estado académico final son observables por HTTP.
    assert own_profile.status_code == 200
    assert own_profile.json()["roles"][0]["name"] == "Estudiante"
    assert forbidden_admin_list.status_code == 401
    assert (subject.status_code, period.status_code) == (201, 201)
    assert enrollment.status_code == 201
    assert grade.status_code == 201
    assert api_client.get("/grades/").json() == [grade.json()]

    assert api_client.post("/auth/logout").status_code == 200
    assert api_client.get("/users/").status_code == 401
