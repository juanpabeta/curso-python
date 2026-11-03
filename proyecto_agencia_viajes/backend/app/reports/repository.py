from sqlalchemy import func
from sqlalchemy.orm import Session
from app.inquiries.models import InquiryModel


class SqlReportReader:
    def __init__(self, db: Session):
        self.db = db

    def monthly(self):
        month = func.date_trunc("month", InquiryModel.created_at)
        return self.db.query(month, func.count()).group_by(month).all()

    def conversion(self):
        return {"won": 0, "lost": 0}

    def inactive_clients(self):
        return []
