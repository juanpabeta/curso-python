from pydantic import BaseModel, ConfigDict
from app.interactions.models import InteractionKind


class InteractionRequest(BaseModel):
    kind: InteractionKind
    content: str


class InteractionResponse(InteractionRequest):
    id: int
    model_config = ConfigDict(from_attributes=True)
    