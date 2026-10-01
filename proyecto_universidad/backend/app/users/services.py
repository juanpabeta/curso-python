from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import DuplicateError, NotFoundError
from app.core.security import hash_password
from app.users.models import Role, User, UserRole
from app.users.schemas import RoleCreate, RoleUpdate, UserCreate, UserUpdate


class UserService:
    """Lógica de negocio para usuarios."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> list[User]:
        return self.db.execute(select(User)).scalars().all()

    def get_by_id(self, user_id: int) -> User:
        user = self.db.get(User, user_id)
        if not user:
            raise NotFoundError(f"Usuario con id {user_id} no encontrado")
        return user

    def create(self, data: UserCreate) -> User:
        existing = self.db.execute(select(User).where(User.email == data.email)).scalar_one_or_none()
        if existing:
            raise DuplicateError("El email ya está registrado")

        user = User(
            email=data.email,
            full_name=data.full_name,
            password_hash=hash_password(data.password),
            is_active=True,
            is_superuser=False,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user_id: int, data: UserUpdate) -> User:
        user = self.get_by_id(user_id)

        if data.email is not None:
            user.email = data.email
        if data.full_name is not None:
            user.full_name = data.full_name
        if data.password is not None:
            user.password_hash = hash_password(data.password)
        if data.is_active is not None:
            user.is_active = data.is_active
        if data.is_superuser is not None:
            user.is_superuser = data.is_superuser

        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user_id: int) -> None:
        user = self.get_by_id(user_id)
        self.db.delete(user)
        self.db.commit()


class RoleService:
    """Lógica de negocio para roles."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> list[Role]:
        return self.db.execute(select(Role)).scalars().all()

    def get_by_id(self, role_id: int) -> Role:
        role = self.db.get(Role, role_id)
        if not role:
            raise NotFoundError(f"Rol con id {role_id} no encontrado")
        return role

    def create(self, data: RoleCreate) -> Role:
        existing = self.db.execute(select(Role).where(Role.name == data.name)).scalar_one_or_none()
        if existing:
            raise DuplicateError("El nombre del rol ya existe")

        role = Role(name=data.name, description=data.description)
        self.db.add(role)
        self.db.commit()
        self.db.refresh(role)
        return role

    def update(self, role_id: int, data: RoleUpdate) -> Role:
        role = self.get_by_id(role_id)

        if data.name is not None:
            role.name = data.name
        if data.description is not None:
            role.description = data.description

        self.db.commit()
        self.db.refresh(role)
        return role

    def delete(self, role_id: int) -> None:
        role = self.get_by_id(role_id)
        self.db.delete(role)
        self.db.commit()

    def assign_role_to_user(self, user_id: int, role_id: int) -> UserRole:
        user = self.db.get(User, user_id)
        if not user:
            raise NotFoundError(f"Usuario con id {user_id} no encontrado")

        role = self.db.get(Role, role_id)
        if not role:
            raise NotFoundError(f"Rol con id {role_id} no encontrado")

        existing = self.db.execute(
            select(UserRole).where(UserRole.user_id == user_id, UserRole.role_id == role_id)
        ).scalar_one_or_none()
        if existing:
            raise DuplicateError("El usuario ya tiene asignado ese rol")

        relation = UserRole(user_id=user_id, role_id=role_id)
        self.db.add(relation)
        self.db.commit()
        self.db.refresh(relation)
        return relation
