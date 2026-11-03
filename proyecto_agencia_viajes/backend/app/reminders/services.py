from app.reminders.exceptions import ReminderNotFound
from app.reminders.models import ReminderModel
from app.reminders.ports import ReminderRepository


def schedule_reminder(repository: ReminderRepository, reminder: ReminderModel):
    return repository.add(reminder)


def complete_reminder(repository: ReminderRepository, reminder_id: int):
    reminder = repository.get(reminder_id)
    if reminder is None:
        raise ReminderNotFound("Recordatorio no encontrado")
    reminder.completed = True
    return repository.update(reminder)


def list_due_reminders(repository: ReminderRepository, now):
    return repository.list_due(now)
