"""Contrato HTTP de tareas académicas usado por la suite Cypress."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.users.models import Role
from app.users.schemas import UserCreate
from app.users.services import UserService

pytestmark = pytest.mark.integration


def _student_headers(api_client: TestClient, db_session: Session) -> dict[str, str]:
    user = UserService(db_session).create(
        UserCreate(
            email="task-student@universidad.test",
            full_name="Estudiante Tareas",
            password="Secret123!",
        ),
    )
    role = Role(name="Estudiante", description="Rol estudiante")
    user.roles.append(role)
    db_session.commit()

    login = api_client.post(
        "/auth/login",
        json={"email": user.email, "password": "Secret123!"},
    )
    assert login.status_code == 200
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


def test_task_lifecycle_persists_and_is_owner_scoped(
    api_client: TestClient,
    db_session: Session,
) -> None:
    headers = _student_headers(api_client, db_session)

    created = api_client.post("/tasks/", json={"title": "Leer el capítulo 4"}, headers=headers)
    assert created.status_code == 201
    body = created.json()
    assert body["title"] == "Leer el capítulo 4"
    assert body["completed"] is False

    listed = api_client.get("/tasks/", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]

    fetched = api_client.get(f"/tasks/{body['id']}", headers=headers)
    assert fetched.status_code == 200
    assert fetched.json()["title"] == "Leer el capítulo 4"

    invalid = api_client.post("/tasks/", json={"title": "   "}, headers=headers)
    assert invalid.status_code == 422

    anonymous = api_client.get("/tasks/")
    assert anonymous.status_code == 401
