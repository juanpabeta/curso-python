from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class LoginRequest(BaseModel):
    """Credenciales de acceso. Rechaza espacios para evitar input manipulado."""

    email: str
    password: str = Field(..., min_length=8, max_length=128)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        if value != value.strip() or any(ch.isspace() for ch in value):
            raise ValueError("El email no puede contener espacios")
        if value.count("@") != 1:
            raise ValueError("El email debe incluir un símbolo @ y un dominio válido")
        local, domain = value.split("@", 1)
        if not local or not domain or "." not in domain:
            raise ValueError("El email debe incluir un correo válido")
        return value.lower()


class TokenResponse(BaseModel):
    """Respuesta pública de autenticación."""

    access_token: str
    token_type: str = "bearer"


class CurrentUserResponse(BaseModel):
    """Perfil de sesión expuesto a la SPA."""

    id: int
    email: str
    full_name: str
    roles: list[str]
