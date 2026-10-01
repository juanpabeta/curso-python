from fastapi import APIRouter, status

from app.core.dependencies import DBSessionDep
from app.subjects.schemas import SubjectCreate, SubjectResponse, SubjectUpdate
from app.subjects.services import SubjectService

router = APIRouter(prefix="/subjects", tags=["subjects"])


@router.get("/", response_model=list[SubjectResponse], status_code=status.HTTP_200_OK)
def list_subjects(db: DBSessionDep) -> list[SubjectResponse]:
    """Lista todas las materias."""
    service = SubjectService(db)
    return service.get_all()


@router.get("/{subject_id}", response_model=SubjectResponse, status_code=status.HTTP_200_OK)
def get_subject(subject_id: int, db: DBSessionDep) -> SubjectResponse:
    """Obtiene una materia por identificador."""
    service = SubjectService(db)
    return service.get_by_id(subject_id)


@router.post("/", response_model=SubjectResponse, status_code=status.HTTP_201_CREATED)
def create_subject(payload: SubjectCreate, db: DBSessionDep) -> SubjectResponse:
    """Crea una nueva materia."""
    service = SubjectService(db)
    return service.create(payload)


@router.put("/{subject_id}", response_model=SubjectResponse, status_code=status.HTTP_200_OK)
def update_subject(subject_id: int, payload: SubjectUpdate, db: DBSessionDep) -> SubjectResponse:
    """Actualiza una materia."""
    service = SubjectService(db)
    return service.update(subject_id, payload)


@router.delete("/{subject_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subject(subject_id: int, db: DBSessionDep) -> None:
    """Elimina una materia."""
    service = SubjectService(db)
    service.delete(subject_id)
    return None
