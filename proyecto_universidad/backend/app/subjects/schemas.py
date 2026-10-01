from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class SubjectBase(BaseModel):
    """Esquema base para materias."""

    code: str = Field(..., min_length=2, max_length=20)
    name: str = Field(..., min_length=2, max_length=200)
    credits: int = Field(..., ge=1, le=12)
    description: str | None = Field(default=None, max_length=500)


class SubjectCreate(SubjectBase):
    """Esquema para registrar una materia."""


class SubjectUpdate(BaseModel):
    """Esquema para actualizar una materia."""

    code: str | None = Field(default=None, min_length=2, max_length=20)
    name: str | None = Field(default=None, min_length=2, max_length=200)
    credits: int | None = Field(default=None, ge=1, le=12)
    description: str | None = Field(default=None, max_length=500)


class SubjectResponse(SubjectBase):
    """Esquema público de respuesta para una materia."""

    id: int
    model_config = ConfigDict(from_attributes=True)
