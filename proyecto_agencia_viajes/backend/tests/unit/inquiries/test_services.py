from app.inquiries.models import InquiryModel, InquiryStage
from app.inquiries.rules import advance, conversion_rate


def test_conversion_rate_is_zero_without_closed_inquiries():
    assert conversion_rate(0, 0) == 0


def test_new_inquiry_can_follow_up():
    assert advance(InquiryModel(client_id=1), InquiryStage.FOLLOWING_UP).stage == InquiryStage.FOLLOWING_UP
