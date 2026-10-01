from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class AcademicPeriodBase(BaseModel):
    """Esquema base para periodo académico."""

    code: str = Field(..., min_length=2, max_length=20)
    name: str = Field(..., min_length=2, max_length=100)
    start_date: date
    end_date: date


class AcademicPeriodCreate(AcademicPeriodBase):
    """Esquema para crear un período académico."""
    code: str
    name: str
    start_date: date
    end_date: date

class AcademicPeriodUpdate(BaseModel):
    """Esquema para actualizar un período académico."""

    code: str | None = Field(default=None, min_length=2, max_length=20)
    name: str | None = Field(default=None, min_length=2, max_length=100)
    start_date: date | None = None
    end_date: date | None = None


class AcademicPeriodResponse(AcademicPeriodBase):
    """Esquema público de respuesta para un período académico."""

    id: int
    model_config = ConfigDict(from_attributes=True)


class EnrollmentBase(BaseModel):
    """Esquema base para inscripciones."""

    user_id: int
    subject_id: int
    period_id: int
    status: str = Field(default="active", min_length=2, max_length=20)


class EnrollmentCreate(EnrollmentBase):
    """Esquema para crear una inscripción."""
    user_id: int
    subject_id: int
    period_id: int
    status: str 

class EnrollmentUpdate(BaseModel):
    """Esquema para actualizar una inscripción."""

    user_id: int | None = None
    subject_id: int | None = None
    period_id: int | None = None
    status: str | None = Field(default=None, min_length=2, max_length=20)


class EnrollmentResponse(EnrollmentBase):
    """Esquema público de respuesta para una inscripción."""

    id: int
    model_config = ConfigDict(from_attributes=True)
