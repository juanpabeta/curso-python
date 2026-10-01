from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import DuplicateError, NotFoundError
from app.enrollments.models import AcademicPeriod, Enrollment
from app.enrollments.schemas import (
    AcademicPeriodCreate,
    AcademicPeriodUpdate,
    EnrollmentCreate,
    EnrollmentUpdate,
)
from app.subjects.models import Subject
from app.users.models import User


class AcademicPeriodService:
    """Lógica de negocio para periodos académicos."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> list[AcademicPeriod]:
        return self.db.execute(select(AcademicPeriod)).scalars().all()

    def get_by_id(self, period_id: int) -> AcademicPeriod:
        period = self.db.get(AcademicPeriod, period_id)
        if not period:
            raise NotFoundError(f"Periodo con id {period_id} no encontrado")
        return period

    def create(self, data: AcademicPeriodCreate) -> AcademicPeriod:
        existing = self.db.execute(select(AcademicPeriod).where(AcademicPeriod.code == data.code)).scalar_one_or_none()
        if existing:
            raise DuplicateError("El código del período académico ya existe")

        period = AcademicPeriod(
            code=data.code,
            name=data.name,
            start_date=data.start_date,
            end_date=data.end_date,
        )
        self.db.add(period)
        self.db.commit()
        self.db.refresh(period)
        return period

    def update(self, period_id: int, data: AcademicPeriodUpdate) -> AcademicPeriod:
        period = self.get_by_id(period_id)

        if data.code is not None:
            period.code = data.code
        if data.name is not None:
            period.name = data.name
        if data.start_date is not None:
            period.start_date = data.start_date
        if data.end_date is not None:
            period.end_date = data.end_date

        self.db.commit()
        self.db.refresh(period)
        return period

    def delete(self, period_id: int) -> None:
        period = self.get_by_id(period_id)
        self.db.delete(period)
        self.db.commit()


class EnrollmentService:
    """Lógica de negocio para inscripciones."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> list[Enrollment]:
        return self.db.execute(select(Enrollment)).scalars().all()

    def get_by_id(self, enrollment_id: int) -> Enrollment:
        enrollment = self.db.get(Enrollment, enrollment_id)
        if not enrollment:
            raise NotFoundError(f"Inscripción con id {enrollment_id} no encontrada")
        return enrollment

    def create(self, data: EnrollmentCreate) -> Enrollment:
        user = self.db.get(User, data.user_id)
        if not user:
            raise NotFoundError(f"Usuario con id {data.user_id} no encontrado")

        subject = self.db.get(Subject, data.subject_id)
        if not subject:
            raise NotFoundError(f"Materia con id {data.subject_id} no encontrada")

        period = self.db.get(AcademicPeriod, data.period_id)
        if not period:
            raise NotFoundError(f"Periodo con id {data.period_id} no encontrado")

        existing = self.db.execute(
            select(Enrollment).where(
                Enrollment.user_id == data.user_id,
                Enrollment.subject_id == data.subject_id,
                Enrollment.period_id == data.period_id,
            )
        ).scalar_one_or_none()
        if existing:
            raise DuplicateError("La inscripción ya existe para este usuario, materia y período")

        enrollment = Enrollment(
            user_id=data.user_id,
            subject_id=data.subject_id,
            period_id=data.period_id,
            status=data.status,
        )
        self.db.add(enrollment)
        self.db.commit()
        self.db.refresh(enrollment)
        return enrollment

    def update(self, enrollment_id: int, data: EnrollmentUpdate) -> Enrollment:
        enrollment = self.get_by_id(enrollment_id)

        if data.user_id is not None:
            enrollment.user_id = data.user_id
        if data.subject_id is not None:
            enrollment.subject_id = data.subject_id
        if data.period_id is not None:
            enrollment.period_id = data.period_id
        if data.status is not None:
            enrollment.status = data.status

        self.db.commit()
        self.db.refresh(enrollment)
        return enrollment

    def delete(self, enrollment_id: int) -> None:
        enrollment = self.get_by_id(enrollment_id)
        self.db.delete(enrollment)
        self.db.commit()
