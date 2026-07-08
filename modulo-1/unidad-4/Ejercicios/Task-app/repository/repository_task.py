from typing import List
from models.model_task import Task
from utils.file_manager import FileManager

class TaskRepository:
    def __init__(self, file_path: str) -> None:
        self._file = FileManager(file_path)
    
    def save(self, task: Task) -> None:
        self._file.append_line(task.serialize())
    
    def get_all(self) -> List[Task]:
        lines = self._file.read_lines()
        return [Task.deserialize(line) for line in lines if line]
    
    def overwrite_all(self, tasks: List[Task]) -> None:
        serialized = [task.serialize() for task in tasks]
        self._file.overwrite_all(serialized)
