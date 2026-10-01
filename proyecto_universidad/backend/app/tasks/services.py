from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError, UnauthorizedError
from app.tasks.models import Task
from app.tasks.schemas import TaskCreate, TaskUpdate


class TaskService:
    """CRUD de tareas con aislamiento por propietario."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def list_for_user(self, user_id: int) -> list[Task]:
        return self.db.execute(select(Task).where(Task.user_id == user_id).order_by(Task.title)).scalars().all()

    def get_owned(self, task_id: str, user_id: int) -> Task:
        task = self.db.get(Task, task_id)
        if not task:
            raise NotFoundError(f"Tarea con id {task_id} no encontrada")
        if task.user_id != user_id:
            raise UnauthorizedError("No tiene permisos para acceder a este recurso")
        return task

    def create(self, user_id: int, data: TaskCreate) -> Task:
        task = Task(title=data.title, completed=False, user_id=user_id)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def update(self, task_id: str, user_id: int, data: TaskUpdate) -> Task:
        task = self.get_owned(task_id, user_id)
        if data.title is not None:
            task.title = data.title
        if data.completed is not None:
            task.completed = data.completed
        self.db.commit()
        self.db.refresh(task)
        return task

    def toggle(self, task_id: str, user_id: int) -> Task:
        task = self.get_owned(task_id, user_id)
        task.completed = not task.completed
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task_id: str, user_id: int) -> None:
        task = self.get_owned(task_id, user_id)
        self.db.delete(task)
        self.db.commit()
