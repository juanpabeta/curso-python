from fastapi import APIRouter, Response, status

from app.auth.schemas import LoginRequest, TokenResponse
from app.auth.services import AuthService
from app.core.config import settings
from app.core.dependencies import DBSessionDep

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login(payload: LoginRequest, db: DBSessionDep, response: Response) -> TokenResponse:
    """Autentica un usuario y devuelve un token JWT con cookie segura por ambiente."""
    service = AuthService(db)
    token = service.login(payload)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=settings.access_token_expire_minutes * 60,
        samesite="lax",
        secure=settings.app_cookie_secure,
    )
    return TokenResponse(access_token=token)


@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(response: Response) -> dict[str, str]:
    """Cierra la sesión del usuario eliminando la cookie de autenticación."""
    response.delete_cookie(key="access_token", secure=settings.app_cookie_secure)
    return {"detail": "Sesión cerrada correctamente"}
