from functools import partial

from fastapi import Depends
from sqlalchemy.orm import Session

from app.auth.services import get_authenticated_user, login_user
from app.clients.repository import SqlClientRepository
from app.clients.services import add_companion, delete_client, register_client, search_clients, update_client
from app.core.database import get_db
from app.inquiries.repository import SqlInquiryRepository
from app.inquiries.services import advance_inquiry, list_inquiries, open_inquiry
from app.interactions.repository import SqlInteractionRepository
from app.interactions.services import list_interactions, record_interaction
from app.reminders.repository import SqlReminderRepository
from app.reminders.services import complete_reminder, list_due_reminders, schedule_reminder
from app.reports.repository import SqlReportReader
from app.reports.services import conversion_report, inactive_clients_report, monthly_inquiry_report
from app.users.ports import UserRepository
from app.users.repository import SqlUserRepository


def _users(db: Session) -> UserRepository:
    return SqlUserRepository(db)


def get_login_service(db: Session = Depends(get_db)):
    return partial(login_user, _users(db))


def get_current_user_service(db: Session = Depends(get_db)):
    return partial(get_authenticated_user, _users(db))


def get_register_client_service(db: Session = Depends(get_db)):
    return partial(register_client, SqlClientRepository(db))


def get_search_clients_service(db: Session = Depends(get_db)):
    return partial(search_clients, SqlClientRepository(db))


def get_client_service(db: Session = Depends(get_db)):
    return partial(SqlClientRepository(db).get)


def get_update_client_service(db: Session = Depends(get_db)):
    return partial(update_client, SqlClientRepository(db))


def get_delete_client_service(db: Session = Depends(get_db)):
    return partial(delete_client, SqlClientRepository(db))


def get_add_companion_service(db: Session = Depends(get_db)):
    return partial(add_companion, SqlClientRepository(db))


def get_record_interaction_service(db: Session = Depends(get_db)):
    return partial(record_interaction, SqlInteractionRepository(db))


def get_list_interactions_service(db: Session = Depends(get_db)):
    return partial(list_interactions, SqlInteractionRepository(db))


def get_open_inquiry_service(db: Session = Depends(get_db)):
    return partial(open_inquiry, SqlInquiryRepository(db))


def get_list_inquiries_service(db: Session = Depends(get_db)):
    return partial(list_inquiries, SqlInquiryRepository(db))


def get_advance_inquiry_service(db: Session = Depends(get_db)):
    return partial(advance_inquiry, SqlInquiryRepository(db))


def get_inactive_inquiries_service(db: Session = Depends(get_db)):
    return partial(inactive_clients_report, SqlReportReader(db))


def get_schedule_reminder_service(db: Session = Depends(get_db)):
    return partial(schedule_reminder, SqlReminderRepository(db))


def get_list_due_reminders_service(db: Session = Depends(get_db)):
    return partial(list_due_reminders, SqlReminderRepository(db))


def get_complete_reminder_service(db: Session = Depends(get_db)):
    return partial(complete_reminder, SqlReminderRepository(db))


def get_monthly_report_service(db: Session = Depends(get_db)):
    return partial(monthly_inquiry_report, SqlReportReader(db))


def get_conversion_report_service(db: Session = Depends(get_db)):
    return partial(conversion_report, SqlReportReader(db))


def get_inactive_clients_report_service(db: Session = Depends(get_db)):
    return partial(inactive_clients_report, SqlReportReader(db))
