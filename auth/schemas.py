from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator


class LoginRequest(BaseModel):
    """Credenciales para autenticación."""

    email: str
    password: str = Field(..., min_length=8, max_length=128)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        """Valida un correo electrónico sin rechazar dominios de prueba como .test."""
        if not value or value.strip() != value:
            raise ValueError("El email no puede tener espacios al inicio o al final")
        normalized = value.strip().lower()
        if "@" not in normalized or normalized.count("@") != 1:
            raise ValueError("El email debe tener un formato válido")
        local, domain = normalized.split("@", 1)
        if not local or not domain or "." not in domain:
            raise ValueError("El email debe incluir dominio válido")
        if any(ch.isspace() for ch in normalized):
            raise ValueError("El email no puede contener espacios")
        return normalized


class TokenResponse(BaseModel):
    """Respuesta con token de acceso."""

    access_token: str
    token_type: str = "bearer"
    model_config = ConfigDict(from_attributes=True)
