from fastapi import FastAPI

from app.auth.routes import router as auth_router
from app.clients.routes import router as clients_router
from app.core.error_handlers import register_error_handlers
from app.inquiries.routes import router as inquiries_router
from app.interactions.routes import router as interactions_router
from app.reminders.routes import router as reminders_router
from app.reports.routes import router as reports_router

app = FastAPI(title="Itinera CRM")
register_error_handlers(app)
app.include_router(auth_router)
app.include_router(clients_router)
app.include_router(inquiries_router)
app.include_router(interactions_router)
app.include_router(reminders_router)
app.include_router(reports_router)
