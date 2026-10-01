from fastapi import APIRouter, Depends, status

from app.core.dependencies import DBSessionDep, require_roles
from app.users.schemas import (
    RoleCreate,
    RoleResponse,
    RoleUpdate,
    UserCreate,
    UserResponse,
    UserUpdate,
)
from app.users.services import RoleService, UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
def list_users(
    db: DBSessionDep,
    _current_user=Depends(require_roles("Administrador", "Docente")),
) -> list[UserResponse]:
    """Lista todos los usuarios."""
    service = UserService(db)
    return service.get_all()


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user(
    user_id: int,
    db: DBSessionDep,
    _current_user=Depends(require_roles("Administrador", "Docente", "Estudiante")),
) -> UserResponse:
    """Obtiene un usuario por identificador."""
    service = UserService(db)
    return service.get_by_id(user_id)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    db: DBSessionDep,
    _current_user=Depends(require_roles("Administrador")),
) -> UserResponse:
    """Crea un nuevo usuario."""
    service = UserService(db)
    return service.create(payload)


@router.put("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user(
    user_id: int,
    payload: UserUpdate,
    db: DBSessionDep,
    _current_user=Depends(require_roles("Administrador", "Docente")),
) -> UserResponse:
    """Actualiza un usuario."""
    service = UserService(db)
    return service.update(user_id, payload)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: DBSessionDep,
    _current_user=Depends(require_roles("Administrador")),
) -> None:
    """Elimina un usuario."""
    service = UserService(db)
    service.delete(user_id)
    return None


role_router = APIRouter(prefix="/roles", tags=["roles"])


@role_router.get("/", response_model=list[RoleResponse], status_code=status.HTTP_200_OK)
def list_roles(
    db: DBSessionDep,
    _current_user=Depends(require_roles("Administrador")),
) -> list[RoleResponse]:
    """Lista todos los roles."""
    service = RoleService(db)
    return service.get_all()


@role_router.get("/{role_id}", response_model=RoleResponse, status_code=status.HTTP_200_OK)
def get_role(
    role_id: int,
    db: DBSessionDep,
    _current_user=Depends(require_roles("Administrador")),
) -> RoleResponse:
    """Obtiene un rol por identificador."""
    service = RoleService(db)
    return service.get_by_id(role_id)


@role_router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
def create_role(
    payload: RoleCreate,
    db: DBSessionDep,
    _current_user=Depends(require_roles("Administrador")),
) -> RoleResponse:
    """Crea un nuevo rol."""
    service = RoleService(db)
    return service.create(payload)


@role_router.put("/{role_id}", response_model=RoleResponse, status_code=status.HTTP_200_OK)
def update_role(
    role_id: int,
    payload: RoleUpdate,
    db: DBSessionDep,
    _current_user=Depends(require_roles("Administrador")),
) -> RoleResponse:
    """Actualiza un rol."""
    service = RoleService(db)
    return service.update(role_id, payload)


@role_router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(
    role_id: int,
    db: DBSessionDep,
    _current_user=Depends(require_roles("Administrador")),
) -> None:
    """Elimina un rol."""
    service = RoleService(db)
    service.delete(role_id)
    return None


@router.post("/{user_id}/roles/{role_id}", status_code=status.HTTP_201_CREATED)
def assign_role_to_user(
    user_id: int,
    role_id: int,
    db: DBSessionDep,
    _current_user=Depends(require_roles("Administrador")),
) -> dict[str, str]:
    """Asigna un rol a un usuario."""
    service = RoleService(db)
    service.assign_role_to_user(user_id, role_id)
    return {"detail": "Rol asignado correctamente"}
