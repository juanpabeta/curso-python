from functools import lru_cache
from typing import Any

from pydantic import AliasChoices, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración segura y diferenciada por entorno."""

    app_name: str = "Universidad API"
    app_version: str = "1.0.0"
    app_env: str = Field(
        default="development",
        validation_alias=AliasChoices("APP_ENV", "ENV", "app_env"),
    )
    app_jwt_secret: str = Field(
        default="change-me-super-secret-key-at-least-32-bytes",
        validation_alias=AliasChoices("APP_JWT_SECRET", "JWT_SECRET_KEY", "JWT_SECRET", "app_jwt_secret"),
    )
    app_cookie_secure: bool = Field(
        default=False,
        validation_alias=AliasChoices("APP_COOKIE_SECURE", "COOKIE_SECURE", "app_cookie_secure"),
    )
    app_cors_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost:3000", "http://127.0.0.1:3000"],
        validation_alias=AliasChoices("APP_CORS_ORIGINS", "CORS_ORIGINS", "app_cors_origins"),
    )
    database_url: str = Field(
        default="postgresql+psycopg://postgres:JP1806@localhost:5432/universidad",
        validation_alias=AliasChoices("DATABASE_URL", "database_url"),
    )
    jwt_secret_key: str = Field(
        default="change-me-super-secret-key-at-least-32-bytes",
        validation_alias=AliasChoices("JWT_SECRET_KEY", "APP_JWT_SECRET", "jwt_secret_key"),
    )
    jwt_algorithm: str = Field(
        default="HS256",
        validation_alias=AliasChoices("JWT_ALGORITHM", "jwt_algorithm"),
    )
    access_token_expire_minutes: int = Field(
        default=60,
        validation_alias=AliasChoices(
            "ACCESS_TOKEN_EXPIRE_MINUTES",
            "JWT_EXPIRATION",
            "JWT_EXPIRATION_MINUTES",
            "access_token_expire_minutes",
        ),
    )
    admin_username: str | None = Field(
        default=None,
        validation_alias=AliasChoices("ADMIN_USERNAME", "admin_username"),
    )
    admin_password: str | None = Field(
        default=None,
        validation_alias=AliasChoices("ADMIN_PASSWORD", "admin_password"),
    )
    allowed_hosts: list[str] = Field(default_factory=lambda: ["*"])

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def is_production(self) -> bool:
        """Indica si la aplicación está ejecutándose en producción."""
        return self.app_env.lower() == "production"

    @field_validator("app_cors_origins", "allowed_hosts", mode="before")
    @classmethod
    def parse_csv_list(cls, value: Any) -> Any:
        """Acepta listas o cadenas separadas por comas desde variables de entorno."""
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()