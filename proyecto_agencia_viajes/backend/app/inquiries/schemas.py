from datetime import datetime

from pydantic import BaseModel
from app.inquiries.models import InquiryStage


class InquiryCreate(BaseModel):
    client_id: int
    stage: InquiryStage = InquiryStage.NEW

class InquiryUpdate(BaseModel):
    client_id: int | None = None
    stage: InquiryStage | None = None
    
class InquiryResponse(BaseModel):
    id: int
    client_id: int
    stage: InquiryStage
    created_at: datetime

    model_config = {"from_attributes": True}




