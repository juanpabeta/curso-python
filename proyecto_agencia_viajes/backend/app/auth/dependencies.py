from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.container import get_current_user_service

bearer = HTTPBearer(auto_error=False)


def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
    service=Depends(get_current_user_service),
):
    token = request.cookies.get("access_token") or (
        credentials.credentials if credentials else None
    )
    if not token:
        raise HTTPException(status_code=401, detail="Autenticación requerida")
    return service(token)
