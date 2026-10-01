"""Pruebas unitarias de autenticación, RBAC y ownership."""

from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from fastapi.security import HTTPAuthorizationCredentials
from starlette.requests import Request

from app.core.dependencies import (
    _normalize_roles,
    get_current_user,
    require_owner_or_role,
    require_roles,
)
from app.core.exceptions import UnauthorizedError

pytestmark = [pytest.mark.unit, pytest.mark.security]


def _request(*, path_params: dict[str, str] | None = None, cookie: str | None = None) -> Request:
    headers = []
    if cookie:
        headers.append((b"cookie", f"access_token={cookie}".encode()))
    scope = {
        "type": "http",
        "method": "GET",
        "path": "/resource",
        "headers": headers,
        "path_params": path_params or {},
    }
    return Request(scope)


def test_normalize_roles_ignores_case_spaces_and_empty_values() -> None:
    # Arrange / Act
    normalized = _normalize_roles([" Administrador ", "DOCENTE", "", "  "])

    # Assert
    assert normalized == {"administrador", "docente"}


def test_require_roles_allows_matching_role_case_insensitively() -> None:
    current_user = SimpleNamespace(roles=[SimpleNamespace(name="administrador")])

    authorized = require_roles("Administrador")(current_user=current_user)

    assert authorized is current_user


def test_require_roles_without_restrictions_accepts_authenticated_user() -> None:
    current_user = SimpleNamespace(roles=[])

    authorized = require_roles()(current_user=current_user)

    assert authorized is current_user


def test_require_roles_rejects_user_without_required_role() -> None:
    current_user = SimpleNamespace(roles=[SimpleNamespace(name="Estudiante")])

    with pytest.raises(UnauthorizedError, match="permisos suficientes"):
        require_roles("Administrador")(current_user=current_user)


@pytest.mark.parametrize(
    ("credentials", "cookie", "expected_token"),
    [
        (HTTPAuthorizationCredentials(scheme="Bearer", credentials="header-token"), None, "header-token"),
        (None, "cookie-token", "cookie-token"),
    ],
)
def test_get_current_user_accepts_bearer_or_cookie(
    monkeypatch: pytest.MonkeyPatch,
    credentials: HTTPAuthorizationCredentials | None,
    cookie: str | None,
    expected_token: str,
) -> None:
    db = MagicMock()
    user = SimpleNamespace(id=7, is_active=True)
    db.get.return_value = user
    decode = MagicMock(return_value={"sub": "7"})
    monkeypatch.setattr("app.core.dependencies.decode_access_token", decode)

    authenticated = get_current_user(
        request=_request(cookie=cookie),
        db=db,
        credentials=credentials,
    )

    assert authenticated is user
    decode.assert_called_once_with(expected_token)
    db.get.assert_called_once()


def test_get_current_user_prefers_bearer_over_cookie(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    db = MagicMock()
    db.get.return_value = SimpleNamespace(id=3, is_active=True)
    decode = MagicMock(return_value={"sub": "3"})
    monkeypatch.setattr("app.core.dependencies.decode_access_token", decode)

    get_current_user(
        request=_request(cookie="cookie-token"),
        db=db,
        credentials=HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials="header-token",
        ),
    )

    decode.assert_called_once_with("header-token")


def test_get_current_user_rejects_missing_token() -> None:
    with pytest.raises(UnauthorizedError, match="No se proporcionó"):
        get_current_user(request=_request(), db=MagicMock(), credentials=None)


def test_get_current_user_rejects_token_without_subject(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("app.core.dependencies.decode_access_token", lambda _token: {})

    with pytest.raises(UnauthorizedError, match="Token inválido"):
        get_current_user(
            request=_request(),
            db=MagicMock(),
            credentials=HTTPAuthorizationCredentials(
                scheme="Bearer",
                credentials="token",
            ),
        )


@pytest.mark.parametrize("user", [None, SimpleNamespace(id=5, is_active=False)])
def test_get_current_user_rejects_missing_or_inactive_user(
    monkeypatch: pytest.MonkeyPatch,
    user,
) -> None:
    db = MagicMock()
    db.get.return_value = user
    monkeypatch.setattr(
        "app.core.dependencies.decode_access_token",
        lambda _token: {"sub": "5"},
    )

    with pytest.raises(UnauthorizedError, match="no encontrado o inactivo"):
        get_current_user(
            request=_request(),
            db=db,
            credentials=HTTPAuthorizationCredentials(
                scheme="Bearer",
                credentials="token",
            ),
        )


def test_owner_or_role_allows_privileged_role() -> None:
    current_user = SimpleNamespace(
        id=1,
        roles=[SimpleNamespace(name="Administrador")],
    )

    authorized = require_owner_or_role("Administrador")(
        request=_request(path_params={"user_id": "99"}),
        db=MagicMock(),
        current_user=current_user,
    )

    assert authorized is current_user


def test_owner_or_role_allows_direct_user_id_match() -> None:
    current_user = SimpleNamespace(id=9, roles=[])

    authorized = require_owner_or_role("Administrador")(
        request=_request(path_params={"user_id": "9"}),
        db=MagicMock(),
        current_user=current_user,
    )

    assert authorized is current_user


def test_owner_or_role_allows_owned_resource() -> None:
    model = type("OwnedRecord", (), {})
    current_user = SimpleNamespace(id=4, roles=[])
    db = MagicMock()
    db.get.return_value = SimpleNamespace(user_id=4)

    authorized = require_owner_or_role(
        "Administrador",
        param_name="enrollment_id",
        model=model,
    )(
        request=_request(path_params={"enrollment_id": "12"}),
        db=db,
        current_user=current_user,
    )

    assert authorized is current_user
    db.get.assert_called_once_with(model, 12)


def test_owner_or_role_rejects_non_owner_without_role() -> None:
    model = type("OwnedRecord", (), {})
    current_user = SimpleNamespace(id=4, roles=[])
    db = MagicMock()
    db.get.return_value = SimpleNamespace(user_id=8)

    with pytest.raises(UnauthorizedError, match="No tiene permisos"):
        require_owner_or_role(
            "Administrador",
            param_name="enrollment_id",
            model=model,
        )(
            request=_request(path_params={"enrollment_id": "12"}),
            db=db,
            current_user=current_user,
        )
