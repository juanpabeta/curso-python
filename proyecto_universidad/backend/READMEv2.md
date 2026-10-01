# Backend Universidad Digital

## Descripción del sistema

El backend de Universidad Digital gestiona la información académica de una institución universitaria. Proporciona endpoints seguros para autenticar usuarios, administrar roles, registrar estudiantes y docentes, gestionar materias, inscripciones y calificaciones.

## Arquitectura aplicada

Se implementa una estructura modular por dominio conservando principios de Clean Architecture y SRP:

- app/core: configuración, base de datos, seguridad, dependencias y excepciones globales.
- app/auth: autenticación y emisión de tokens JWT.
- app/users: gestión de usuarios y roles.
- app/subjects: administración de materias.
- app/enrollments: inscripciones y periodos académicos.
- app/grades: calificaciones por inscripción.
- app/main.py: bootstrap de la aplicación y manejo global de errores.

## Estructura de carpetas

```text
backend/
├── app/
│   ├── auth/
│   │   ├── routes.py
│   │   ├── schemas.py
│   │   └── services.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── dependencies.py
│   │   ├── exceptions.py
│   │   └── security.py
│   ├── enrollments/
│   │   ├── models.py
│   │   ├── routes.py
│   │   ├── schemas.py
│   │   └── services.py
│   ├── grades/
│   │   ├── models.py
│   │   ├── routes.py
│   │   ├── schemas.py
│   │   └── services.py
│   ├── subjects/
│   │   ├── models.py
│   │   ├── routes.py
│   │   ├── schemas.py
│   │   └── services.py
│   ├── users/
│   │   ├── models.py
│   │   ├── routes.py
│   │   ├── schemas.py
│   │   └── services.py
│   ├── __init__.py
│   └── main.py
├── .env
├── README.md
├── READMEv2.md
├── requirements.txt
└── tests/
    └── test_auth_flow.py
```

## Seguridad implementada

- Hashing seguro de contraseñas con bcrypt.
- Emisión de JWT con algoritmo HS256.
- Validación de tokens en dependencias de seguridad.
- Soporte para flujo con Header Authorization o cookies HttpOnly.
- Rutas protegidas por roles con enfoque de mínimo privilegio.
- Excepciones personalizadas para autenticación, no encontrado y duplicados.
- Manejo centralizado de errores para respuestas HTTP coherentes.

## Flujo de autenticación

1. El usuario envía email y contraseña a /auth/login.
2. El sistema valida credenciales y estado del usuario.
3. Si son válidas, emite un JWT y guarda la cookie access_token.
4. Las rutas protegidas validan el token con get_current_user.
5. El acceso adicional se restringe con require_roles().

## Roles y permisos

Roles soportados:

- Administrador
- Docente
- Estudiante

Reglas de acceso:

- Administrador: acceso completo.
- Docente: gestión académica y consulta de usuarios.
- Estudiante: consulta de su propia información y recursos autorizados.

## Cómo levantar el backend

### 1. Crear entorno virtual

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

Crear un archivo .env con valores como:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/universidad
JWT_SECRET_KEY=tu_secreto_super_seguro
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 4. Ejecutar la aplicación

```bash
uvicorn app.main:app --reload
```

## Variables de entorno

- DATABASE_URL
- JWT_SECRET_KEY
- JWT_ALGORITHM
- ACCESS_TOKEN_EXPIRE_MINUTES

## Endpoints principales

### Autenticación

- POST /auth/login
- POST /auth/logout

### Usuarios

- GET /users/
- GET /users/{user_id}
- POST /users/
- PUT /users/{user_id}
- DELETE /users/{user_id}

### Roles

- GET /roles/
- GET /roles/{role_id}
- POST /roles/
- PUT /roles/{role_id}
- DELETE /roles/{role_id}

### Materias

- GET /subjects/
- GET /subjects/{subject_id}
- POST /subjects/
- PUT /subjects/{subject_id}
- DELETE /subjects/{subject_id}

### Inscripciones

- GET /enrollments/
- GET /enrollments/{enrollment_id}
- POST /enrollments/
- PUT /enrollments/{enrollment_id}
- DELETE /enrollments/{enrollment_id}

### Periodos académicos

- GET /periods/
- GET /periods/{period_id}
- POST /periods/
- PUT /periods/{period_id}
- DELETE /periods/{period_id}

### Calificaciones

- GET /grades/
- GET /grades/{grade_id}
- POST /grades/
- PUT /grades/{grade_id}
- DELETE /grades/{grade_id}

## Próximos pasos

- Añadir tests de integración reales para cada dominio.
- Incluir migraciones con Alembic para PostgreSQL.
- Implementar autorización fina por recursos y ownership.
- Preparar documentación OpenAPI para frontend.
- Integrar validaciones y auditoría avanzadas.
