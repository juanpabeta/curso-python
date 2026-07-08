from repository.repository_task import TaskRepository
from models.model_task import Task
from utils.validator import validate_title, validate_index
from typing import List

class TaskService:
    def __init__(self, repository: TaskRepository) -> None:
        self._repository = repository
        
    def create_task(self, title: str) -> None:
        clean_title = validate_title(title)
        task = Task(clean_title)
        self._repository.save(task)
    
    def list_tasks(self) -> list[Task]:
        return self._repository.get_all()
    
    def complete_task(self, index: int) -> None:
        tasks = self._repository.get_all()
        validated_index = validate_index(index, len(tasks))
        updated_task = tasks[validated_index].mark_completed()
        tasks[validated_index] = updated_task
        self._repository.overwrite_all(tasks)
        