from sqlalchemy.orm import Session
from app.inquiries.models import InquiryModel


class SqlInquiryRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, inquiry: InquiryModel) -> InquiryModel:
        row = InquiryModel(client_id=inquiry.client_id, stage=inquiry.stage)
        self.db.add(row); self.db.commit(); self.db.refresh(row)
        return row

    def get(self, inquiry_id: int) -> InquiryModel | None:
        row = self.db.get(InquiryModel, inquiry_id)
        return row

    def update(self, inquiry: InquiryModel) -> InquiryModel:
        row = self.db.get(InquiryModel, inquiry.id); row.stage = inquiry.stage
        self.db.commit(); self.db.refresh(row)
        return row

    def list(self) -> list[InquiryModel]:
        return self.db.query(InquiryModel).all()

    def delete(self, inquiry_id: int) -> None:
        row = self.db.get(InquiryModel, inquiry_id)
        if row is not None:
            self.db.delete(row)
            self.db.commit()