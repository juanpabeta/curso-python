from sqlalchemy.orm import Session
from app.reminders.models import ReminderModel


class SqlReminderRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, item: ReminderModel) -> ReminderModel:
        row = ReminderModel(client_id=item.client_id, due_at=item.due_at)
        self.db.add(row); self.db.commit(); self.db.refresh(row)
        return row

    def get(self, item_id):
        row = self.db.get(ReminderModel, item_id)
        return row

    def update(self, item):
        row = self.db.get(ReminderModel, item.id); row.completed = item.completed
        self.db.commit(); self.db.refresh(row)
        return row

    def list_due(self, now):
        return self.db.query(ReminderModel).filter(
            ReminderModel.due_at <= now,
            ReminderModel.completed.is_(False),
        ).all()
