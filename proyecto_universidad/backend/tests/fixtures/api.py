"""Clientes API reales y cliente con autenticación sustituida."""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.main import app
from app.users.models import User


@pytest.fixture
def api_client(db_session: Session) -> Generator[TestClient, None, None]:
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    client.close()
    app.dependency_overrides.clear()


@pytest.fixture
def simulated_auth_client(
    db_session: Session,
    admin_user: User,
) -> Generator[TestClient, None, None]:
    """Cliente para aislar autorización en tests de rutas; no usar en E2E."""

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = lambda: admin_user
    client = TestClient(app)
    yield client
    client.close()
    app.dependency_overrides.clear()


@pytest.fixture
def auth_headers(api_client: TestClient, admin_user: User) -> dict[str, str]:
    response = api_client.post(
        "/auth/login",
        json={"email": admin_user.email, "password": "Secret123!"},
    )
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['access_token']}"}
