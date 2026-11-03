from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SqlEnum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class InteractionKind(str, Enum):
    CALL = "CALL"
    MESSAGE = "MESSAGE"
    EMAIL = "EMAIL"
    VISIT = "VISIT"
    NOTE = "NOTE"


class InteractionModel(Base):
    __tablename__ = "interactions"
    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(Integer)
    kind: Mapped[InteractionKind] = mapped_column(SqlEnum(InteractionKind))
    content: Mapped[str] = mapped_column(String(2000))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)