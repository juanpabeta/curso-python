from datetime import datetime, timezone

from fastapi import APIRouter, Depends, status
from app.auth.dependencies import get_current_user

from app.container import (
    get_complete_reminder_service,
    get_list_due_reminders_service,
    get_schedule_reminder_service,
)
from app.reminders.models import ReminderModel
from app.reminders.schemas import ReminderCreate, ReminderResponse

router = APIRouter(
    prefix="/reminders",
    tags=["reminders"],
    dependencies=[Depends(get_current_user)],
)


@router.post("", response_model=ReminderResponse, status_code=status.HTTP_201_CREATED)
def create(request: ReminderCreate, service=Depends(get_schedule_reminder_service)):
    return service(ReminderModel(client_id=request.client_id, due_at=request.due_at))


@router.get("/due", response_model=list[ReminderResponse])
def due(service=Depends(get_list_due_reminders_service)):
    return service(datetime.now(timezone.utc))


@router.patch("/{reminder_id}/complete", response_model=ReminderResponse)
def complete(reminder_id: int, service=Depends(get_complete_reminder_service)):
    return service(reminder_id)
