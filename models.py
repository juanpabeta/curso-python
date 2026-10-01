from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.grades.models import Grade
    from app.subjects.models import Subject
    from app.users.models import User


class AcademicPeriod(Base):
    """Periodo académico."""

    __tablename__ = "academic_periods"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String(20), nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)

    enrollments: Mapped[list["Enrollment"]] = relationship(back_populates="academic_period")


class Enrollment(Base):
    """Inscripción del estudiante a una materia en un periodo."""

    __tablename__ = "enrollments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"), nullable=False)
    period_id: Mapped[int] = mapped_column(ForeignKey("academic_periods.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="active", nullable=False)

    user: Mapped["User"] = relationship(back_populates="enrollments")
    subject: Mapped["Subject"] = relationship(back_populates="enrollments")
    academic_period: Mapped["AcademicPeriod"] = relationship(back_populates="enrollments")
    grades: Mapped[list["Grade"]] = relationship(back_populates="enrollment")
