from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings


class Base(DeclarativeBase):
    """Base declarativa para todos los modelos SQLAlchemy."""


engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    """Obtener la sesión de base de datos para la petición."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
