from app.inquiries.exceptions import InquiryNotFound
from app.inquiries.models import InquiryModel, InquiryStage
from app.inquiries.ports import InquiryRepository, ContactHistory, InactivityPolicy
from app.inquiries.rules import advance


def open_inquiry(repository: InquiryRepository, inquiry: InquiryModel) -> InquiryModel:
    return repository.add(inquiry)


def advance_inquiry(repository: InquiryRepository, inquiry_id: int, stage: InquiryStage) -> InquiryModel:
    inquiry = repository.get(inquiry_id)
    if inquiry is None:
        raise InquiryNotFound("Consulta no encontrada")
    return repository.update(advance(inquiry, stage))


def list_inquiries(repository: InquiryRepository) -> list[InquiryModel]:
    return repository.list()


def list_inquiries_without_contact(
    repository: InquiryRepository,
    history: ContactHistory,
    policy: InactivityPolicy,
) -> list[InquiryModel]:
    return [i for i in repository.list() if policy.is_inactive(history.last_contact(i.client_id))]
