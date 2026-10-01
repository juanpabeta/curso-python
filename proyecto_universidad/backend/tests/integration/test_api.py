"""Integración HTTP + dependencias + servicios + serialización."""

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

pytestmark = pytest.mark.integration


def test_health_and_logout_contract(api_client: TestClient) -> None:
    assert api_client.get("/health").json() == {"status": "ok"}
    response = api_client.post("/auth/logout")
    assert response.status_code == 200
    assert response.json()["detail"] == "Sesión cerrada correctamente"


def test_user_endpoint_serializes_public_fields_only(
    simulated_auth_client: TestClient,
) -> None:
    response = simulated_auth_client.post("/users/", json=user_data())
    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "student@universidad.test"
    assert body["roles"] == []
    assert "password" not in body
    assert "password_hash" not in body


def test_subject_api_crud_and_validation(simulated_auth_client: TestClient) -> None:
    created = simulated_auth_client.post("/subjects/", json=subject_data())
    assert created.status_code == 201
    subject_id = created.json()["id"]

    listed = simulated_auth_client.get("/subjects/")
    assert listed.status_code == 200
    assert listed.json()[0]["code"] == "TST101"

    fetched = simulated_auth_client.get(f"/subjects/{subject_id}")
    assert fetched.status_code == 200

    updated = simulated_auth_client.put(
        f"/subjects/{subject_id}",
        json={"name": "Testing avanzado", "credits": 5},
    )
    assert updated.status_code == 200
    assert updated.json()["credits"] == 5

    invalid = simulated_auth_client.post(
        "/subjects/",
        json=subject_data(code="BAD", credits=-1),
    )
    assert invalid.status_code == 422

    deleted = simulated_auth_client.delete(f"/subjects/{subject_id}")
    assert deleted.status_code == 204
    assert simulated_auth_client.get(f"/subjects/{subject_id}").status_code == 404


@pytest.mark.security
def test_protected_endpoint_rejects_missing_and_tampered_tokens(
    api_client: TestClient,
) -> None:
    without_token = api_client.get("/users/")
    tampered = api_client.get(
        "/users/",
        headers={"Authorization": "Bearer not.a.valid-token"},
    )
    assert without_token.status_code == 401
    assert tampered.status_code == 401


@pytest.mark.security
def test_sql_injection_string_is_data_not_a_query(
    simulated_auth_client: TestClient,
) -> None:
    payload = subject_data(
        code="QA';DROP",
        name="Robert'); DROP TABLE subjects;--",
    )
    created = simulated_auth_client.post("/subjects/", json=payload)
    assert created.status_code == 201
    assert simulated_auth_client.get("/subjects/").json()[0]["name"] == payload["name"]


def test_complete_crud_surface_is_connected(
    simulated_auth_client: TestClient,
    admin_user,
) -> None:
    """Smoke de todos los adaptadores HTTP; las reglas se prueban por separado."""
    client = simulated_auth_client

    # Usuarios
    user = client.post(
        "/users/",
        json=user_data(email="crud@universidad.test"),
    ).json()
    assert client.get("/users/").status_code == 200
    assert client.get(f"/users/{user['id']}").status_code == 200
    changed_user = client.put(
        f"/users/{user['id']}",
        json={
            "email": "changed@universidad.test",
            "full_name": "Nombre Cambiado",
            "password": "ChangedPass123!",
            "is_active": False,
            "is_superuser": True,
        },
    )
    assert changed_user.json()["is_active"] is False
    assert client.delete(f"/users/{user['id']}").status_code == 204

    # Roles y asignación
    role = client.post(
        "/roles/",
        json={"name": "Auditor", "description": "Rol temporal"},
    ).json()
    assert client.get("/roles/").status_code == 200
    assert client.get(f"/roles/{role['id']}").status_code == 200
    changed_role = client.put(
        f"/roles/{role['id']}",
        json={"name": "Auditor QA", "description": "Actualizado"},
    )
    assert changed_role.json()["name"] == "Auditor QA"
    assert client.post(f"/users/{admin_user.id}/roles/{role['id']}").status_code == 201
    assert client.post(f"/users/{admin_user.id}/roles/{role['id']}").status_code == 409
    disposable_role = client.post(
        "/roles/",
        json={"name": "Temporal", "description": None},
    ).json()
    assert client.delete(f"/roles/{disposable_role['id']}").status_code == 204

    # Materia, periodo, matrícula y calificación.
    subject = client.post("/subjects/", json=subject_data(code="CRUD101")).json()
    period = client.post("/periods/", json=period_data(code="CRUD-2026")).json()
    assert client.get("/periods/").status_code == 200
    assert client.get(f"/periods/{period['id']}").status_code == 200
    changed_period = client.put(
        f"/periods/{period['id']}",
        json={
            "code": "CRUD-2026-B",
            "name": "Periodo actualizado",
            "start_date": "2026-02-01",
            "end_date": "2026-07-01",
        },
    )
    assert changed_period.json()["code"] == "CRUD-2026-B"

    record = client.post(
        "/enrollments/",
        json={
            "user_id": admin_user.id,
            "subject_id": subject["id"],
            "period_id": period["id"],
            "status": "active",
        },
    ).json()
    assert client.get(f"/enrollments/{record['id']}").status_code == 200
    changed_record = client.put(
        f"/enrollments/{record['id']}",
        json={
            "user_id": admin_user.id,
            "subject_id": subject["id"],
            "period_id": period["id"],
            "status": "completed",
        },
    )
    assert changed_record.json()["status"] == "completed"

    grade = client.post(
        "/grades/",
        json={
            "enrollment_id": record["id"],
            "type": "Parcial",
            "score": 80,
            "comments": "Inicial",
        },
    ).json()
    assert client.get(f"/grades/{grade['id']}").status_code == 200
    changed_grade = client.put(
        f"/grades/{grade['id']}",
        json={
            "enrollment_id": record["id"],
            "type": "Final",
            "score": 95,
            "comments": "Actualizada",
        },
    )
    assert changed_grade.json()["score"] == 95
    assert client.delete(f"/grades/{grade['id']}").status_code == 204
    assert client.delete(f"/enrollments/{record['id']}").status_code == 204
    assert client.delete(f"/periods/{period['id']}").status_code == 204


@pytest.mark.parametrize(
    "path",
    [
        "/users/999",
        "/roles/999",
        "/subjects/999",
        "/periods/999",
        "/enrollments/999",
        "/grades/999",
    ],
)
def test_resource_detail_returns_404_for_unknown_id(
    simulated_auth_client: TestClient,
    path: str,
) -> None:
    response = simulated_auth_client.get(path)

    assert response.status_code == 404
    assert "no encontr" in response.json()["detail"].lower()


@pytest.mark.parametrize(
    ("path", "payload"),
    [
        ("/users/", user_data(email="invalid")),
        ("/roles/", role_data(name="")),
        ("/subjects/", subject_data(credits=0)),
        ("/periods/", period_data(start_date="not-a-date")),
        (
            "/enrollments/",
            {"user_id": None, "subject_id": 1, "period_id": 1, "status": "active"},
        ),
        ("/grades/", grade_data(enrollment_id=1, score=101)),
    ],
)
def test_create_endpoints_return_422_for_invalid_payload(
    simulated_auth_client: TestClient,
    path: str,
    payload: dict,
) -> None:
    response = simulated_auth_client.post(path, json=payload)

    assert response.status_code == 422
    assert response.json()["detail"]


@pytest.mark.parametrize(
    ("path", "payload"),
    [
        ("/users/", user_data()),
        ("/roles/", role_data(name="Duplicado")),
        ("/subjects/", subject_data()),
        ("/periods/", period_data()),
    ],
)
def test_unique_resources_return_409_when_created_twice(
    simulated_auth_client: TestClient,
    path: str,
    payload: dict,
) -> None:
    first = simulated_auth_client.post(path, json=payload)
    duplicate = simulated_auth_client.post(path, json=payload)

    assert first.status_code == 201
    assert duplicate.status_code == 409


def test_academic_api_rejects_missing_relations_with_404(
    simulated_auth_client: TestClient,
) -> None:
    enrollment_response = simulated_auth_client.post(
        "/enrollments/",
        json=enrollment_data(user_id=999, subject_id=999, period_id=999),
    )
    grade_response = simulated_auth_client.post(
        "/grades/",
        json=grade_data(enrollment_id=999),
    )

    assert enrollment_response.status_code == 404
    assert "Usuario" in enrollment_response.json()["detail"]
    assert grade_response.status_code == 404
    assert "Inscripción" in grade_response.json()["detail"]


def test_partial_updates_preserve_omitted_fields(
    simulated_auth_client: TestClient,
    admin_user,
) -> None:
    subject = simulated_auth_client.post(
        "/subjects/",
        json=subject_data(code="PATCH101"),
    ).json()
    period = simulated_auth_client.post(
        "/periods/",
        json=period_data(code="PATCH-2026"),
    ).json()
    enrollment = simulated_auth_client.post(
        "/enrollments/",
        json=enrollment_data(admin_user.id, subject["id"], period["id"]),
    ).json()
    grade = simulated_auth_client.post(
        "/grades/",
        json=grade_data(enrollment["id"], score=70),
    ).json()

    changed_subject = simulated_auth_client.put(
        f"/subjects/{subject['id']}",
        json={"name": "Nombre actualizado"},
    ).json()
    changed_enrollment = simulated_auth_client.put(
        f"/enrollments/{enrollment['id']}",
        json={"status": "completed"},
    ).json()
    changed_grade = simulated_auth_client.put(
        f"/grades/{grade['id']}",
        json={"score": 90},
    ).json()

    assert changed_subject["code"] == subject["code"]
    assert changed_subject["credits"] == subject["credits"]
    assert changed_enrollment["subject_id"] == subject["id"]
    assert changed_grade["type"] == grade["type"]
    assert changed_grade["score"] == 90
