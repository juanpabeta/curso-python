from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.enrollments.models import Enrollment
from app.grades.models import Grade
from app.grades.schemas import GradeCreate, GradeUpdate


class GradeService:
    """Lógica de negocio para calificaciones."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> list[Grade]:
        return self.db.execute(select(Grade)).scalars().all()

    def get_by_id(self, grade_id: int) -> Grade:
        grade = self.db.get(Grade, grade_id)
        if not grade:
            raise NotFoundError(f"Calificación con id {grade_id} no encontrada")
        return grade

    def create(self, data: GradeCreate) -> Grade:
        enrollment = self.db.get(Enrollment, data.enrollment_id)
        if not enrollment:
            raise NotFoundError(f"Inscripción con id {data.enrollment_id} no encontrada")

        grade = Grade(
            enrollment_id=data.enrollment_id,
            type=data.type,
            score=data.score,
            comments=data.comments,
        )
        self.db.add(grade)
        self.db.commit()
        self.db.refresh(grade)
        return grade

    def update(self, grade_id: int, data: GradeUpdate) -> Grade:
        grade = self.get_by_id(grade_id)

        if data.enrollment_id is not None:
            grade.enrollment_id = data.enrollment_id
        if data.type is not None:
            grade.type = data.type
        if data.score is not None:
            grade.score = data.score
        if data.comments is not None:
            grade.comments = data.comments

        self.db.commit()
        self.db.refresh(grade)
        return grade

    def delete(self, grade_id: int) -> None:
        grade = self.get_by_id(grade_id)
        self.db.delete(grade)
        self.db.commit()
