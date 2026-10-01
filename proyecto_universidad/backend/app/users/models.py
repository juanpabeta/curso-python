from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from app.core.database import Base

if TYPE_CHECKING:
    from app.enrollments.models import Enrollment


class Role(Base):
    """Rol del sistema."""

    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    users: Mapped[list["User"]] = relationship(back_populates="roles", secondary="user_roles")


class User(Base):
    """Usuario del sistema."""

    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("email", name="uq_users_email"),)

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(default=False, nullable=False)

    roles: Mapped[list[Role]] = relationship(back_populates="users", secondary="user_roles")
    enrollments: Mapped[list["Enrollment"]] = relationship(back_populates="user")

    @property
    def role_names(self) -> list[str]:
        """Devuelve los nombres de los roles del usuario."""
        return [role.name for role in self.roles]

    @validates("email")
    def validate_email(self, key: str, value: str) -> str:
        """Normaliza el email para evitar duplicidades por mayúsculas y espacios."""
        return value.strip().lower()


class UserRole(Base):
    """Relación muchos a muchos entre usuarios y roles."""

    __tablename__ = "user_roles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)

    __table_args__ = (UniqueConstraint("user_id", "role_id", name="uq_user_roles"),)


