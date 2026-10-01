from typing import Annotated

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import UnauthorizedError
from app.core.security import decode_access_token
from app.users.models import User

security = HTTPBearer(auto_error=False)
DBSessionDep = Annotated[Session, Depends(get_db)]
CurrentUserDep = Annotated[User, Depends(lambda: None)]


def _normalize_roles(values: set[str] | list[str]) -> set[str]:
    """Normaliza nombres de roles para comparar sin distinguir mayúsculas."""
    return {value.strip().lower() for value in values if value and value.strip()}


def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> User:
    """Obtiene el usuario autenticado a partir del token JWT."""
    token = None
    if credentials:
        token = credentials.credentials
    if not token:
        token = request.cookies.get("access_token")
    if not token:
        raise UnauthorizedError("No se proporcionó un token de autenticación")

    payload = decode_access_token(token)
    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedError("Token inválido")

    user = db.get(User, int(user_id))
    if not user or not user.is_active:
        raise UnauthorizedError("Usuario no encontrado o inactivo")
    return user


def require_roles(*allowed_roles: str):
    """Valida que el usuario autenticado tenga alguno de los roles permitidos."""

    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if not allowed_roles:
            return current_user

        role_names = _normalize_roles([role.name for role in current_user.roles])
        normalized_allowed = _normalize_roles(allowed_roles)
        if not role_names.intersection(normalized_allowed):
            raise UnauthorizedError("No tiene permisos suficientes para acceder a este recurso")
        return current_user

    return role_checker


def require_owner_or_role(*allowed_roles: str, param_name: str = "user_id", owner_field: str = "user_id", model: type | None = None):
    """Permite acceso por rol o por propiedad del recurso para un usuario concreto."""

    def owner_checker(
        request: Request,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ) -> User:
        if current_user.roles and _normalize_roles([role.name for role in current_user.roles]).intersection(
            _normalize_roles(allowed_roles)
        ):
            return current_user

        resource_id = request.path_params.get(param_name)
        if resource_id is not None:
            if model is not None:
                record = db.get(model, int(resource_id))
                if record and getattr(record, owner_field, None) == current_user.id:
                    return current_user
            if current_user.id == int(resource_id):
                return current_user

        raise UnauthorizedError("No tiene permisos para acceder a este recurso")

    return owner_checker


CurrentUserDep = Annotated[User, Depends(get_current_user)]
