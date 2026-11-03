from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.core.config import settings
from app.auth.exceptions import InvalidCredentials
from app.users.models import UserModel
from app.users.ports import UserRepository


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def _verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode(), password_hash.encode())


def _create_token(subject: str) -> str:
    expires = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    return jwt.encode({"sub": subject, "exp": expires}, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def _decode_token(token: str) -> str:
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        return str(payload["sub"])
    except (jwt.PyJWTError, KeyError) as exc:
        raise InvalidCredentials("Token inválido") from exc


def login_user(users: UserRepository, username: str, password: str) -> str:
    user = users.get_by_username(username)
    if user is None or not user.is_active or not _verify_password(password, user.password_hash):
        raise InvalidCredentials("Credenciales inválidas")
    return _create_token(str(user.id))


def get_authenticated_user(users: UserRepository, token: str) -> UserModel:
    try:
        user_id = int(_decode_token(token))
    except (TypeError, ValueError):
        raise InvalidCredentials("Token inválido") from None
    user = users.get(user_id)
    if user is None:
        raise InvalidCredentials("Usuario no encontrado")
    return user
