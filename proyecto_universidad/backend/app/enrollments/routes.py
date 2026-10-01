from fastapi import APIRouter, status

from app.core.dependencies import DBSessionDep
from app.enrollments.schemas import (
    AcademicPeriodCreate,
    AcademicPeriodResponse,
    AcademicPeriodUpdate,
    EnrollmentCreate,
    EnrollmentResponse,
    EnrollmentUpdate,
)
from app.enrollments.services import AcademicPeriodService, EnrollmentService

router = APIRouter(prefix="/enrollments", tags=["enrollments"])


@router.get("/", response_model=list[EnrollmentResponse], status_code=status.HTTP_200_OK)
def list_enrollments(db: DBSessionDep) -> list[EnrollmentResponse]:
    """Lista todas las inscripciones."""
    service = EnrollmentService(db)
    return service.get_all()


@router.get("/{enrollment_id}", response_model=EnrollmentResponse, status_code=status.HTTP_200_OK)
def get_enrollment(enrollment_id: int, db: DBSessionDep) -> EnrollmentResponse:
    """Obtiene una inscripción por identificador."""
    service = EnrollmentService(db)
    return service.get_by_id(enrollment_id)


@router.post("/", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
def create_enrollment(payload: EnrollmentCreate, db: DBSessionDep) -> EnrollmentResponse:
    """Crea una inscripción."""
    service = EnrollmentService(db)
    return service.create(payload)


@router.put("/{enrollment_id}", response_model=EnrollmentResponse, status_code=status.HTTP_200_OK)
def update_enrollment(enrollment_id: int, payload: EnrollmentUpdate, db: DBSessionDep) -> EnrollmentResponse:
    """Actualiza una inscripción."""
    service = EnrollmentService(db)
    return service.update(enrollment_id, payload)


@router.delete("/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_enrollment(enrollment_id: int, db: DBSessionDep) -> None:
    """Elimina una inscripción."""
    service = EnrollmentService(db)
    service.delete(enrollment_id)
    return None


period_router = APIRouter(prefix="/periods", tags=["academic-periods"])


@period_router.get("/", response_model=list[AcademicPeriodResponse], status_code=status.HTTP_200_OK)
def list_periods(db: DBSessionDep) -> list[AcademicPeriodResponse]:
    """Lista todos los períodos académicos."""
    service = AcademicPeriodService(db)
    return service.get_all()


@period_router.get("/{period_id}", response_model=AcademicPeriodResponse, status_code=status.HTTP_200_OK)
def get_period(period_id: int, db: DBSessionDep) -> AcademicPeriodResponse:
    """Obtiene un período académico por identificador."""
    service = AcademicPeriodService(db)
    return service.get_by_id(period_id)


@period_router.post("/", response_model=AcademicPeriodResponse, status_code=status.HTTP_201_CREATED)
def create_period(payload: AcademicPeriodCreate, db: DBSessionDep) -> AcademicPeriodResponse:
    """Crea un periodo académico."""
    service = AcademicPeriodService(db)
    return service.create(payload)


@period_router.put("/{period_id}", response_model=AcademicPeriodResponse, status_code=status.HTTP_200_OK)
def update_period(period_id: int, payload: AcademicPeriodUpdate, db: DBSessionDep) -> AcademicPeriodResponse:
    """Actualiza un periodo académico."""
    service = AcademicPeriodService(db)
    return service.update(period_id, payload)


@period_router.delete("/{period_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_period(period_id: int, db: DBSessionDep) -> None:
    """Elimina un período académico."""
    service = AcademicPeriodService(db)
    service.delete(period_id)
    return None
