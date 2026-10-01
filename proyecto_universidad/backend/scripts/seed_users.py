"""Crea usuarios de desarrollo para entrar al sistema.

El primer administrador no puede nacer por API: POST /users/ exige el rol
Administrador. Este script carga roles y usuarios en la base configurada
en .env (idempotente: no duplica si ya existen).

Ejecutar desde backend/:

    python -m scripts.seed_users
"""

from __future__ import annotations

from sqlalchemy import select

from app.core.database import Base, SessionLocal, engine
from app.core.security import hash_password
from app.enrollments.models import AcademicPeriod, Enrollment  # noqa: F401
from app.grades.models import Grade  # noqa: F401
from app.subjects.models import Subject  # noqa: F401
from app.tasks.models import Task  # noqa: F401
from app.users.models import Role, User, UserRole

DEV_PASSWORD = "Secret123!"

DEV_USERS = (
    {
        "email": "admin@universidad.test",
        "full_name": "Administrador Universidad",
        "role": "Administrador",
        "is_superuser": True,
    },
    {
        "email": "teacher@universidad.test",
        "full_name": "Docente Universidad",
        "role": "Docente",
        "is_superuser": False,
    },
    {
        "email": "student@universidad.test",
        "full_name": "Estudiante Universidad",
        "role": "Estudiante",
        "is_superuser": False,
    },
)


def _get_or_create_role(db, name: str) -> Role:
    role = db.execute(select(Role).where(Role.name == name)).scalar_one_or_none()
    if role:
        return role
    role = Role(name=name, description=f"Rol {name}")
    db.add(role)
    db.flush()
    return role


def _get_or_create_user(db, email: str, full_name: str, is_superuser: bool) -> User:
    user = db.execute(select(User).where(User.email == email)).scalar_one_or_none()
    if user:
        user.full_name = full_name
        user.is_active = True
        user.is_superuser = is_superuser
        user.password_hash = hash_password(DEV_PASSWORD)
        db.flush()
        return user

    user = User(
        email=email,
        full_name=full_name,
        password_hash=hash_password(DEV_PASSWORD),
        is_active=True,
        is_superuser=is_superuser,
    )
    db.add(user)
    db.flush()
    return user


def seed() -> list[str]:
    """Crea roles y usuarios de desarrollo. Devuelve los emails asegurados."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    created: list[str] = []
    try:
        for item in DEV_USERS:
            role = _get_or_create_role(db, item["role"])
            user = _get_or_create_user(db, item["email"], item["full_name"], item["is_superuser"])
            assigned = db.execute(
                select(UserRole).where(UserRole.user_id == user.id, UserRole.role_id == role.id)
            ).scalar_one_or_none()
            if not assigned:
                db.add(UserRole(user_id=user.id, role_id=role.id))
            created.append(item["email"])
        db.commit()
        return created
    finally:
        db.close()


if __name__ == "__main__":
    emails = seed()
    print("Usuarios de desarrollo listos.")
    print(f"Contraseña común: {DEV_PASSWORD}")
    for email in emails:
        print(f"  - {email}")
