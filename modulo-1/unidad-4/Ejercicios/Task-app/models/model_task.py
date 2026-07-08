from dataclasses import dataclass

@dataclass(frozen=True)
class Task:
    title: str
    completed: bool = False
    
    def serialize(self)  -> str:
        return f"{self.title}|{int(self.completed)}"
    
    @staticmethod
    def deserialize(data: str) -> "Task":
        title, completed = data.split("|")
        return Task(title=title, completed=bool(int(completed)))
    
    def mark_completed(self)->"Task":
        return Task(title=self.title, completed=True)