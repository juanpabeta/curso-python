from app.inquiries.exceptions import InvalidStageTransition
from app.inquiries.models import InquiryModel, InquiryStage


def advance(inquiry: InquiryModel, stage: InquiryStage) -> InquiryModel:
    allowed = {InquiryStage.NEW: {InquiryStage.FOLLOWING_UP, InquiryStage.LOST}, InquiryStage.FOLLOWING_UP: {InquiryStage.WON, InquiryStage.LOST}}
    current_stage = inquiry.stage or InquiryStage.NEW
    if stage not in allowed.get(current_stage, set()):
        raise InvalidStageTransition("Transición de etapa inválida")
    inquiry.stage = stage
    return inquiry


def conversion_rate(won: int, lost: int) -> float:
    return won / (won + lost) if won + lost else 0.0
