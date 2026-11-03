
from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SqlEnum, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class InquiryStage(str, Enum):
    NEW = "NEW"
    FOLLOWING_UP = "FOLLOWING_UP"
    WON = "WON"
    LOST = "LOST"
    
class InquiryModel(Base):
    __tablename__ = "inquiries"
    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(Integer)
    stage: Mapped[InquiryStage] = mapped_column(SqlEnum(InquiryStage), default=InquiryStage.NEW)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)