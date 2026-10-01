from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.auth.routes import router as auth_router
from app.core.config import settings
from app.core.database import Base, engine
from app.core.exceptions import AppError
from app.enrollments.routes import period_router
from app.enrollments.routes import router as enrollment_router
from app.grades.routes import router as grade_router
from app.subjects.routes import router as subject_router
from app.tasks.models import Task  # noqa: F401 - registra metadata
from app.tasks.routes import router as task_router
from app.users.routes import role_router
from app.users.routes import router as user_router

app = FastAPI(
    title="Universidad API",
    version="1.0.0",
    description="API para gestión académica universitaria",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.app_cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept", "Origin", "X-Requested-With"],
)


@app.on_event("startup")
def create_database() -> None:
    """Crea las tablas al arrancar la aplicación si no existen."""
    Base.metadata.create_all(bind=engine)


@app.exception_handler(AppError)
async def app_error_handler(_request, exc: AppError):
    """Centraliza el manejo de errores de dominio de la aplicación."""
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(role_router)
app.include_router(subject_router)
app.include_router(enrollment_router)
app.include_router(period_router)
app.include_router(grade_router)
app.include_router(task_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    """Endpoint de verificación del servicio."""
    return {"status": "ok"}
