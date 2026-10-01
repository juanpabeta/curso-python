from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class GradeBase(BaseModel):
    """Esquema base para una calificación."""

    enrollment_id: int
    type: str = Field(..., min_length=2, max_length=50)
    score: float = Field(..., ge=0, le=100)
    comments: str | None = Field(default=None, max_length=500)


class GradeCreate(GradeBase):
    """Esquema para crear una calificación."""


class GradeUpdate(BaseModel):
    """Esquema para actualizar una calificación."""

    enrollment_id: int | None = None
    type: str | None = Field(default=None, min_length=2, max_length=50)
    score: float | None = Field(default=None, ge=0, le=100)
    comments: str | None = Field(default=None, max_length=500)


class GradeResponse(GradeBase):
    """Esquema público de respuesta para una calificación."""

    id: int
    model_config = ConfigDict(from_attributes=True)
