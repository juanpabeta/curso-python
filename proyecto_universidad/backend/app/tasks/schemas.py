from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TaskCreate(BaseModel):
    """Alta de una tarea académica."""

    title: str = Field(..., min_length=1, max_length=120)

    @field_validator("title")
    @classmethod
    def normalize_title(cls, value: str) -> str:
        title = value.strip()
        if not title:
            raise ValueError("El título es obligatorio")
        return title


class TaskUpdate(BaseModel):
    """Actualización parcial de una tarea."""

    title: str | None = Field(default=None, min_length=1, max_length=120)
    completed: bool | None = None

    @field_validator("title")
    @classmethod
    def normalize_title(cls, value: str | None) -> str | None:
        if value is None:
            return value
        title = value.strip()
        if not title:
            raise ValueError("El título es obligatorio")
        return title


class TaskResponse(BaseModel):
    """Contrato público de una tarea."""

    id: str
    title: str
    completed: bool
    model_config = ConfigDict(from_attributes=True)
