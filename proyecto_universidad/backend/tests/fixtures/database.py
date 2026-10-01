"""Fixtures de persistencia: una base SQLite nueva por prueba."""

from collections.abc import Generator
from datetime import date

import pytest
from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base
from app.core.security import hash_password
from app.enrollments.models import AcademicPeriod, Enrollment
from app.grades.models import Grade  # noqa: F401 - registra metadata
from app.subjects.models import Subject
from app.users.models import Role, User


@pytest.fixture
def db_engine() -> Generator[Engine, None, None]:
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    @event.listens_for(engine, "connect")
    def enable_foreign_keys(dbapi_connection, _connection_record) -> None:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def db_session(db_engine: Engine) -> Generator[Session, None, None]:
    session_factory = sessionmaker(bind=db_engine, expire_on_commit=False)
    with session_factory() as session:
        yield session
        session.rollback()


@pytest.fixture
def admin_user(db_session: Session) -> User:
    role = Role(name="Administrador", description="Administrador de pruebas")
    user = User(
        email="admin@universidad.test",
        full_name="Admin Pruebas",
        password_hash=hash_password("Secret123!"),
        is_active=True,
        is_superuser=False,
        roles=[role],
    )
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def valid_user() -> dict[str, str]:
    return {
        "email": "student@universidad.test",
        "full_name": "Estudiante Prueba",
        "password": "SecurePass123!",
    }


@pytest.fixture
def invalid_user() -> dict[str, str]:
    return {"email": "sin-dominio", "full_name": "", "password": "123"}


@pytest.fixture
def course(db_session: Session) -> Subject:
    subject = Subject(code="TST101", name="Testing de Software", credits=4)
    db_session.add(subject)
    db_session.commit()
    return subject


@pytest.fixture
def academic_period(db_session: Session) -> AcademicPeriod:
    period = AcademicPeriod(
        code="2026-1",
        name="Primer semestre 2026",
        start_date=date(2026, 1, 15),
        end_date=date(2026, 6, 15),
    )
    db_session.add(period)
    db_session.commit()
    return period


@pytest.fixture
def enrollment(
    db_session: Session,
    admin_user: User,
    course: Subject,
    academic_period: AcademicPeriod,
) -> Enrollment:
    record = Enrollment(
        user_id=admin_user.id,
        subject_id=course.id,
        period_id=academic_period.id,
        status="active",
    )
    db_session.add(record)
    db_session.commit()
    return record
