from fastapi import APIRouter, status

from app.core.dependencies import DBSessionDep
from app.grades.schemas import GradeCreate, GradeResponse, GradeUpdate
from app.grades.services import GradeService

router = APIRouter(prefix="/grades", tags=["grades"])


@router.get("/", response_model=list[GradeResponse], status_code=status.HTTP_200_OK)
def list_grades(db: DBSessionDep) -> list[GradeResponse]:
    """Lista todas las calificaciones."""
    service = GradeService(db)
    return service.get_all()


@router.get("/{grade_id}", response_model=GradeResponse, status_code=status.HTTP_200_OK)
def get_grade(grade_id: int, db: DBSessionDep) -> GradeResponse:
    """Obtiene una calificación por identificador."""
    service = GradeService(db)
    return service.get_by_id(grade_id)


@router.post("/", response_model=GradeResponse, status_code=status.HTTP_201_CREATED)
def create_grade(payload: GradeCreate, db: DBSessionDep) -> GradeResponse:
    """Crea una calificación."""
    service = GradeService(db)
    return service.create(payload)


@router.put("/{grade_id}", response_model=GradeResponse, status_code=status.HTTP_200_OK)
def update_grade(grade_id: int, payload: GradeUpdate, db: DBSessionDep) -> GradeResponse:
    """Actualiza una calificación."""
    service = GradeService(db)
    return service.update(grade_id, payload)


@router.delete("/{grade_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_grade(grade_id: int, db: DBSessionDep) -> None:
    """Elimina una calificación."""
    service = GradeService(db)
    service.delete(grade_id)
    return None
