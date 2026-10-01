from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.auth.schemas import LoginRequest
from app.core.exceptions import UnauthorizedError
from app.core.security import create_access_token, verify_password
from app.users.models import User


class AuthService:
    """Lógica de negocio para autenticación."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def login(self, payload: LoginRequest) -> str:
        user = self.db.execute(
            select(User)
            .options(selectinload(User.roles))
            .where(User.email == payload.email.lower())
        ).scalar_one_or_none()
        if not user:
            raise UnauthorizedError("Credenciales inválidas")

        if not verify_password(payload.password, user.password_hash):
            raise UnauthorizedError("Credenciales inválidas")

        if not user.is_active:
            raise UnauthorizedError("Usuario inactivo")

        role_names = [role.name for role in user.roles]
        return create_access_token(str(user.id), roles=role_names)
