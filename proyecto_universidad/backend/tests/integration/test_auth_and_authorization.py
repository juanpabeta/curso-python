"""Integración de login real, cookies JWT y matriz RBAC."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.users.models import Role, User
from app.users.schemas import UserCreate
from app.users.services import UserService

pytestmark = [pytest.mark.integration, pytest.mark.security]


def _create_user_with_role(
    db_session: Session,
    *,
    email: str,
    role_name: str,
) -> User:
    user = UserService(db_session).create(
        UserCreate(
            email=email,
            full_name=f"Usuario {role_name}",
            password="Secret123!",
        ),
    )
    role = Role(name=role_name, description=f"Rol {role_name}")
    user.roles.append(role)
    db_session.commit()
    db_session.refresh(user)
    return user


def test_login_sets_http_only_cookie_and_cookie_authenticates(
    api_client: TestClient,
    admin_user: User,
) -> None:
    # Arrange / Act
    login = api_client.post(
        "/auth/login",
        json={"email": admin_user.email, "password": "Secret123!"},
    )
    protected = api_client.get("/users/")

    # Assert
    assert login.status_code == 200
    assert "access_token=" in login.headers["set-cookie"]
    assert "HttpOnly" in login.headers["set-cookie"]
    assert protected.status_code == 200


def test_logout_removes_cookie_and_revokes_client_session(
    api_client: TestClient,
    admin_user: User,
) -> None:
    api_client.post(
        "/auth/login",
        json={"email": admin_user.email, "password": "Secret123!"},
    )

    logout = api_client.post("/auth/logout")
    protected = api_client.get("/users/")

    assert logout.status_code == 200
    assert "access_token=" in logout.headers["set-cookie"]
    assert protected.status_code == 401


@pytest.mark.parametrize(
    "payload",
    [
        {"email": "unknown@universidad.test", "password": "Secret123!"},
        {"email": "admin@universidad.test", "password": "WrongPass123!"},
        {"email": "not-an-email", "password": "Secret123!"},
        {"email": "admin@universidad.test", "password": "short"},
    ],
)
def test_login_rejects_invalid_credentials_or_payload(
    api_client: TestClient,
    admin_user: User,
    payload: dict[str, str],
) -> None:
    response = api_client.post("/auth/login", json=payload)

    assert response.status_code in {401, 422}
    assert "access_token" not in response.json()


def test_expired_token_cannot_access_protected_endpoint(
    api_client: TestClient,
    admin_user: User,
) -> None:
    token = create_access_token(
        str(admin_user.id),
        roles=["Administrador"],
        expires_minutes=-1,
    )

    response = api_client.get(
        "/users/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 401


def test_me_returns_persisted_profile(api_client: TestClient, admin_user: User, auth_headers: dict[str, str]) -> None:
    response = api_client.get("/auth/me", headers=auth_headers)

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == admin_user.id
    assert body["email"] == admin_user.email
    assert body["full_name"] == admin_user.full_name
    assert body["roles"] == ["Administrador"]


def test_me_rejects_anonymous_client(api_client: TestClient) -> None:
    response = api_client.get("/auth/me")

    assert response.status_code == 401
    assert "detail" in response.json()


@pytest.mark.parametrize(
    ("method", "path", "payload"),
    [
        ("GET", "/users/", None),
        (
            "POST",
            "/users/",
            {
                "email": "forbidden@universidad.test",
                "full_name": "Sin permisos",
                "password": "Secret123!",
            },
        ),
        ("GET", "/roles/", None),
    ],
)
def test_student_cannot_use_administrative_endpoints(
    api_client: TestClient,
    db_session: Session,
    method: str,
    path: str,
    payload: dict[str, str] | None,
) -> None:
    student = _create_user_with_role(
        db_session,
        email="student-rbac@universidad.test",
        role_name="Estudiante",
    )
    login = api_client.post(
        "/auth/login",
        json={"email": student.email, "password": "Secret123!"},
    )
    headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

    response = api_client.request(method, path, json=payload, headers=headers)

    assert response.status_code == 401
    assert "permisos suficientes" in response.json()["detail"]


def test_student_can_read_user_detail_allowed_by_current_rbac_contract(
    api_client: TestClient,
    db_session: Session,
) -> None:
    student = _create_user_with_role(
        db_session,
        email="reader@universidad.test",
        role_name="Estudiante",
    )
    login = api_client.post(
        "/auth/login",
        json={"email": student.email, "password": "Secret123!"},
    )

    response = api_client.get(
        f"/users/{student.id}",
        headers={"Authorization": f"Bearer {login.json()['access_token']}"},
    )

    assert response.status_code == 200
    assert response.json()["email"] == student.email
    assert "password_hash" not in response.json()


def test_docente_can_list_users_but_cannot_manage_roles(
    api_client: TestClient,
    db_session: Session,
) -> None:
    teacher = _create_user_with_role(
        db_session,
        email="teacher@universidad.test",
        role_name="Docente",
    )
    login = api_client.post(
        "/auth/login",
        json={"email": teacher.email, "password": "Secret123!"},
    )
    headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

    users_response = api_client.get("/users/", headers=headers)
    roles_response = api_client.get("/roles/", headers=headers)

    assert users_response.status_code == 200
    assert roles_response.status_code == 401
