from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import DuplicateError, NotFoundError,IntegrityConflictError
from app.subjects.models import Subject
from app.subjects.schemas import SubjectCreate, SubjectUpdate
from app.enrollments.models import Enrollment

class SubjectService:
    """Lógica de negocio para materias."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> list[Subject]:
        return self.db.execute(select(Subject)).scalars().all()

    def get_by_id(self, subject_id: int) -> Subject:
        subject = self.db.get(Subject, subject_id)
        if not subject:
            raise NotFoundError(f"Materia con id {subject_id} no encontrada")
        return subject

    def create(self, data: SubjectCreate) -> Subject:
        existing_code = self.db.execute(select(Subject).where(Subject.code == data.code)).scalar_one_or_none()
        if existing_code:
            raise DuplicateError("El código de la materia ya existe")

        subject = Subject(
            code=data.code,
            name=data.name,
            credits=data.credits,
            description=data.description,
        )
        self.db.add(subject)
        self.db.commit()
        self.db.refresh(subject)
        return subject

    def update(self, subject_id: int, data: SubjectUpdate) -> Subject:
        subject = self.get_by_id(subject_id)

        if data.code is not None:
            subject.code = data.code
        if data.name is not None:
            subject.name = data.name
        if data.credits is not None:
            subject.credits = data.credits
        if data.description is not None:
            subject.description = data.description

        self.db.commit()
        self.db.refresh(subject)
        return subject

    def delete(self, subject_id: int) -> None:
        """Elimina una materia si no tiene inscripciones."""
        
        # Buscar la materia
        subject = self.db.query(Subject).filter(
            Subject.id == subject_id
        ).first()
        
        if not subject:
            raise NotFoundError(f"Materia con ID {subject_id} no encontrada")
        
        # Buscar inscripciones relacionadas
        enrollments_count = self.db.query(Enrollment).filter(
            Enrollment.subject_id == subject_id
        ).count()
        
        if enrollments_count > 0:
            raise IntegrityConflictError(
                f"No se puede eliminar la materia '{subject.name}'. "
                f"Hay {enrollments_count} estudiante(s) inscrito(s)"
            )
        
        # Eliminar la materia
        self.db.delete(subject)
        self.db.commit()
