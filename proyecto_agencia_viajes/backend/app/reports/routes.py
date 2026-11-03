from fastapi import APIRouter, Depends
from app.auth.dependencies import get_current_user

from app.container import (
    get_conversion_report_service,
    get_inactive_clients_report_service,
    get_monthly_report_service,
)

router = APIRouter(
    prefix="/reports",
    tags=["reports"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/inquiries-by-month")
def monthly(service=Depends(get_monthly_report_service)):
    return service()


@router.get("/conversion")
def conversion(service=Depends(get_conversion_report_service)):
    return service()


@router.get("/inactive-clients")
def inactive(service=Depends(get_inactive_clients_report_service)):
    return service()
