from datetime import datetime
from pydantic import BaseModel, ConfigDict



class ReminderCreate(BaseModel):
    client_id: int
    due_at: datetime
    completed: bool = False

class ReminderResponse(ReminderCreate):
    id: int
    completed: bool
    model_config = ConfigDict(from_attributes=True)
