from fastapi import APIRouter, Depends, status
from app.auth.dependencies import get_current_user

from app.container import (
    get_advance_inquiry_service,
    get_inactive_inquiries_service,
    get_list_inquiries_service,
    get_open_inquiry_service,
)
from app.inquiries.models import InquiryModel
from app.inquiries.schemas import InquiryCreate, InquiryResponse, InquiryUpdate

router = APIRouter(
    prefix="/inquiries",
    tags=["inquiries"],
    dependencies=[Depends(get_current_user)],
)


@router.get("", response_model=list[InquiryResponse])
def list_all(service=Depends(get_list_inquiries_service)):
    return service()


@router.post("", response_model=InquiryResponse, status_code=status.HTTP_201_CREATED)
def create(request: InquiryCreate, service=Depends(get_open_inquiry_service)):
    return service(InquiryModel(client_id=request.client_id, stage=request.stage))


@router.get("/without-contact", response_model=list[InquiryResponse])
def without_contact(service=Depends(get_inactive_inquiries_service)):
    return service()


@router.patch("/{inquiry_id}/stage", response_model=InquiryResponse)
def change_stage(
    inquiry_id: int,
    request: InquiryUpdate,
    service=Depends(get_advance_inquiry_service),
):
    if request.stage is None:
        return service(inquiry_id, request.stage)
    return service(inquiry_id, request.stage)
