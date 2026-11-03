from fastapi import APIRouter, Depends, Response

from app.auth.dependencies import get_current_user
from app.auth.schemas import LoginRequest, TokenResponse
from app.container import get_current_user_service, get_login_service
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

def _set_access_token_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        secure=settings.app_cookie_secure,
        max_age=settings.access_token_expire_minutes * 60,
    )

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, response: Response, service=Depends(get_login_service)) -> TokenResponse:
    token = service(request.username, request.password)
    _set_access_token_cookie(response, token)
    return TokenResponse(access_token=token)


@router.post("/logout", dependencies=[Depends(get_current_user)])
def logout(response: Response) -> dict[str, str]:
    response.delete_cookie("access_token")
    return {"message": "Sesión cerrada"}


@router.get("/me")
def me(user=Depends(get_current_user)) -> dict[str, object]:
    return {"id": user.id, "username": user.username, "is_active": user.is_active}
