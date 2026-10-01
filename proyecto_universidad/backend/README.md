# Proyecto Universitario - Backend API

## Descripción

Este backend implementa la capa de API para una plataforma de gestión académica universitaria con los dominios principales:

- Usuarios y roles
- Materias
- Inscripciones académicas
- Calificaciones
- Autenticación y autorización

La estructura sigue un enfoque de arquitectura por capas con responsabilidades separadas:

- `app/core`: configuración, seguridad, DB y dependencias globales
- `app/auth`: autenticación y emisión de tokens
- `app/users`: gestión de usuarios y roles
- `app/subjects`: gestión de materias
- `app/enrollments`: gestión de inscripciones y periodos académicos
- `app/grades`: gestión de calificaciones

## Stack

- Python 3.11+
- FastAPI
- SQLAlchemy 2.x
- Pydantic v2
- PostgreSQL 18
- JWT con `python-jose`
- Password hashing con `passlib[bcrypt]`

## Estructura del proyecto

```text
backend/
├── README.md
├── requirements.txt
└── app/
    ├── __init__.py
    ├── main.py
    ├── core/
    │   ├── __init__.py
    │   ├── config.py
    │   ├── database.py
    │   ├── security.py
    │   ├── dependencies.py
    │   └── exceptions.py
    ├── auth/
    │   ├── __init__.py
    │   ├── schemas.py
    │   ├── services.py
    │   └── routes.py
    ├── users/
    │   ├── __init__.py
    │   ├── models.py
    │   ├── schemas.py
    │   ├── services.py
    │   └── routes.py
    ├── subjects/
    │   ├── __init__.py
    │   ├── models.py
    │   ├── schemas.py
    │   ├── services.py
    │   └── routes.py
    ├── enrollments/
    │   ├── __init__.py
    │   ├── models.py
    │   ├── schemas.py
    │   ├── services.py
    │   └── routes.py
    └── grades/
        ├── __init__.py
        ├── models.py
        ├── schemas.py
        ├── services.py
        └── routes.py
```

## Reglas de diseño

- Cada archivo tiene una responsabilidad única.
- La lógica de negocio vive en `services.py`.
- Los endpoints no consultan la base de datos directamente.
- La validación de entradas se hace exclusivamente con Pydantic.
- No se exponen hashes ni datos sensibles.
- Los roles y permisos deben administrarse con enfoque de mínimo privilegio.

## Ejecución

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

En Windows (PowerShell):

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

La API queda en `http://127.0.0.1:8000` y Swagger en `http://127.0.0.1:8000/docs`.

## Usuarios de prueba (desarrollo local)

Al arrancar, la API solo crea tablas vacías. El primer administrador **no se puede crear desde Swagger**: `POST /users/` exige el rol `Administrador`. Por eso existe un seed idempotente.

Desde `backend/`, con el entorno virtual activo y PostgreSQL disponible:

```powershell
python -m scripts.seed_users
```

El script crea (o actualiza) estos usuarios contra la base de `.env`:

| Rol | Email | Contraseña |
| --- | --- | --- |
| Administrador | `admin@universidad.test` | `Secret123!` |
| Docente | `teacher@universidad.test` | `Secret123!` |
| Estudiante | `student@universidad.test` | `Secret123!` |

### Entrar como admin

**Swagger** (`http://127.0.0.1:8000/docs`):

1. `POST /auth/login` con el JSON de abajo.
2. Copiar `access_token` de la respuesta.
3. Pulsar **Authorize** y pegar `Bearer <token>` (o solo el token, según el diálogo).

```json
{
  "email": "admin@universidad.test",
  "password": "Secret123!"
}
```

**Frontend** (`http://localhost:3000/login`): el formulario ya trae esas credenciales de administrador.

Estas cuentas son solo para desarrollo y pruebas. No usarlas en producción.

## Variables de entorno

Definir estas variables antes de ejecutar la API:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/universidad
JWT_SECRET_KEY=cambiar-este-secreto
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## Nota

Este proyecto está estructurado para evolución a un modelo de negocio real, con separación clara entre dominio, aplicación y acceso a datos.
