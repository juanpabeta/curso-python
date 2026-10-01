from fastapi import APIRouter, status

from app.core.dependencies import CurrentUserDep, DBSessionDep
from app.tasks.schemas import TaskCreate, TaskResponse, TaskUpdate
from app.tasks.services import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=list[TaskResponse], status_code=status.HTTP_200_OK)
def list_tasks(db: DBSessionDep, current_user: CurrentUserDep) -> list[TaskResponse]:
    return TaskService(db).list_for_user(current_user.id)


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, db: DBSessionDep, current_user: CurrentUserDep) -> TaskResponse:
    return TaskService(db).create(current_user.id, payload)


@router.get("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def get_task(task_id: str, db: DBSessionDep, current_user: CurrentUserDep) -> TaskResponse:
    return TaskService(db).get_owned(task_id, current_user.id)


@router.patch("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def update_task(
    task_id: str,
    payload: TaskUpdate,
    db: DBSessionDep,
    current_user: CurrentUserDep,
) -> TaskResponse:
    return TaskService(db).update(task_id, current_user.id, payload)


@router.post("/{task_id}/toggle", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def toggle_task(task_id: str, db: DBSessionDep, current_user: CurrentUserDep) -> TaskResponse:
    return TaskService(db).toggle(task_id, current_user.id)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, db: DBSessionDep, current_user: CurrentUserDep) -> None:
    TaskService(db).delete(task_id, current_user.id)
    return None
