from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator


class RoleBase(BaseModel):
    """Esquema base para roles."""

    name: str = Field(..., min_length=2, max_length=50)
    description: str | None = Field(default=None, max_length=255)


class RoleCreate(RoleBase):
    """Esquema para crear un rol."""


class RoleUpdate(BaseModel):
    """Esquema para actualizar un rol."""

    name: str | None = Field(default=None, min_length=2, max_length=50)
    description: str | None = Field(default=None, max_length=255)


class RoleResponse(RoleBase):
    """Esquema público de respuesta para un rol."""

    id: int
    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    """Esquema base para usuarios."""

    email: str
    full_name: str = Field(..., min_length=2, max_length=200)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        """Valida el formato del email sin bloquear dominios de prueba como .test."""
        normalized = value.strip().lower()
        if not normalized or normalized.count("@") != 1:
            raise ValueError("El email debe incluir un símbolo @ y un dominio válido")
        local, domain = normalized.split("@", 1)
        if not local or not domain or "." not in domain:
            raise ValueError("El email debe incluir un dominio válido")
        if any(ch.isspace() for ch in normalized):
            raise ValueError("El email no puede contener espacios")
        return normalized


class UserCreate(UserBase):
    """Esquema para crear un usuario."""

    password: str = Field(..., min_length=8, max_length=128)


class UserUpdate(BaseModel):
    """Esquema para actualizar un usuario."""

    email: str | None = None
    full_name: str | None = Field(default=None, min_length=2, max_length=200)
    password: str | None = Field(default=None, min_length=8, max_length=128)
    is_active: bool | None = None
    is_superuser: bool | None = None

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str | None) -> str | None:
        """Valida el email si se incluye en la actualización."""
        if value is None:
            return value
        normalized = value.strip().lower()
        if not normalized or normalized.count("@") != 1:
            raise ValueError("El email debe incluir un símbolo @ y un dominio válido")
        local, domain = normalized.split("@", 1)
        if not local or not domain or "." not in domain:
            raise ValueError("El email debe incluir un dominio válido")
        if any(ch.isspace() for ch in normalized):
            raise ValueError("El email no puede contener espacios")
        return normalized


class UserResponse(UserBase):
    """Esquema público de respuesta para un usuario."""

    id: int
    is_active: bool
    is_superuser: bool
    roles: list[RoleResponse] = []
    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    """Esquema de login del usuario."""

    email: str
    password: str = Field(..., min_length=8, max_length=128)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        """Valida el formato del email del login."""
        normalized = value.strip().lower()
        if not normalized or normalized.count("@") != 1:
            raise ValueError("El email debe incluir un símbolo @ y un dominio válido")
        local, domain = normalized.split("@", 1)
        if not local or not domain or "." not in domain:
            raise ValueError("El email debe incluir un dominio válido")
        if any(ch.isspace() for ch in normalized):
            raise ValueError("El email no puede contener espacios")
        return normalized
