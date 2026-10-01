from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.schemas import LoginRequest
from app.core.exceptions import UnauthorizedError
from app.core.security import create_access_token, verify_password
from app.users.models import User


class AuthService:
    """Autenticación contra usuarios persistidos."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def login(self, data: LoginRequest) -> str:
        user = self.db.execute(select(User).where(User.email == data.email)).scalar_one_or_none()
        if user is None or not verify_password(data.password, user.password_hash):
            raise UnauthorizedError("Credenciales inválidas")
        if not user.is_active:
            raise UnauthorizedError("Usuario inactivo")

        return create_access_token(str(user.id), roles=[role.name for role in user.roles])
