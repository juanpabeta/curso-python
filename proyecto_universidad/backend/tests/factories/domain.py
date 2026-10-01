"""Factories deterministas para construir datos válidos con overrides."""

from datetime import date
from typing import Any


def user_data(**overrides: Any) -> dict[str, Any]:
    defaults = {
        "email": "student@universidad.test",
        "full_name": "Estudiante Prueba",
        "password": "SecurePass123!",
    }
    return defaults | overrides


def subject_data(**overrides: Any) -> dict[str, Any]:
    defaults = {
        "code": "TST101",
        "name": "Materia de prueba",
        "credits": 4,
        "description": "Dato generado por una factory determinista",
    }
    return defaults | overrides


def period_data(**overrides: Any) -> dict[str, Any]:
    defaults = {
        "code": "2026-1",
        "name": "Periodo de prueba",
        "start_date": date(2026, 1, 15).isoformat(),
        "end_date": date(2026, 6, 15).isoformat(),
    }
    return defaults | overrides


def enrollment_data(user_id: int, subject_id: int, period_id: int, **overrides: Any) -> dict[str, Any]:
    defaults = {
        "user_id": user_id,
        "subject_id": subject_id,
        "period_id": period_id,
        "status": "active",
    }
    return defaults | overrides


def role_data(**overrides: Any) -> dict[str, Any]:
    defaults = {
        "name": "Estudiante",
        "description": "Rol generado por una factory determinista",
    }
    return defaults | overrides


def grade_data(enrollment_id: int, **overrides: Any) -> dict[str, Any]:
    defaults = {
        "enrollment_id": enrollment_id,
        "type": "Final",
        "score": 85.0,
        "comments": "Calificación generada por una factory determinista",
    }
    return defaults | overrides
