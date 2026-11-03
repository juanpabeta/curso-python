from sqlalchemy.orm import Session
from app.interactions.models import InteractionModel


class SqlInteractionRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, item: InteractionModel) -> InteractionModel:
        row = InteractionModel(client_id=item.client_id, kind=item.kind, content=item.content)
        self.db.add(row); self.db.commit(); self.db.refresh(row)
        return row

    def list(self, client_id: int) -> list[InteractionModel]:
        return self.db.query(InteractionModel).filter_by(client_id=client_id).all()

    def last_contact(self, client_id: int):
        row = self.db.query(InteractionModel).filter_by(client_id=client_id).order_by(InteractionModel.created_at.desc()).first()
        return row.created_at if row else None
