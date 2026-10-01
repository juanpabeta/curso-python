from fastapi import APIRouter, Response
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.auth.schemas import CurrentUserResponse, LoginRequest, TokenResponse
from app.auth.services import AuthService
from app.core.config import settings
from app.core.dependencies import CurrentUserDep, DBSessionDep
from app.users.models import User

router = APIRouter(prefix="/auth", tags=["auth"])


def _set_access_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=settings.app_cookie_secure,
        samesite="lax",
        path="/",
        max_age=settings.access_token_expire_minutes * 60,
    )


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, response: Response, db: DBSessionDep) -> TokenResponse:
    token = AuthService(db).login(payload)
    _set_access_cookie(response, token)
    return TokenResponse(access_token=token, token_type="bearer")


@router.get("/me", response_model=CurrentUserResponse)
def read_current_user(current_user: CurrentUserDep, db: DBSessionDep) -> CurrentUserResponse:
    """Perfil persistido. La SPA lo usa para restaurar nombre, correo y roles."""
    user = db.execute(
        select(User).where(User.id == current_user.id).options(selectinload(User.roles))
    ).scalar_one()
    return CurrentUserResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        roles=[role.name for role in user.roles],
    )


@router.post("/logout")
def logout(response: Response) -> dict[str, str]:
    response.delete_cookie(
        key="access_token",
        path="/",
        samesite="lax",
        secure=settings.app_cookie_secure,
    )
    return {"detail": "Sesión cerrada correctamente"}



