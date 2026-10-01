# README_TEST — Validación manual de APIs

## 1. Introducción

Este documento tiene como objetivo guiar la validación manual de las APIs del backend de Universidad Digital. Está orientado a consumo real de endpoints, no a pruebas automatizadas.

Una API queda validada cuando:

- responde con los códigos HTTP esperados,
- acepta payloads correctos y rechaza errores de negocio,
- protege recursos por autenticación y autorización,
- devuelve respuestas consistentes y sin datos sensibles,
- se puede probar desde Swagger UI, Postman o cURL.

Este documento cubre únicamente pruebas manuales del backend, no pruebas unitarias ni automatizadas.

---

## 2. Herramientas recomendadas

### Swagger UI

Es la opción más rápida para revisar y consumir la API de forma visual.

- URL: http://localhost:8000/docs
- Ideal para:
  - ver schemas,
  - probar endpoints sin escribir demasiada lógica,
  - validar payloads y respuestas.

### Postman

Es ideal para pruebas de flujo completo, autenticación y reutilización de variables.

- Ideal para:
  - colecciones,
  - headers,
  - cookies,
  - pruebas de seguridad y permisos.

### cURL

Es útil para pruebas rápidas desde terminal.

- Ideal para:
  - validación directa,
  - automatización básica manual,
  - debugging de endpoints.

---

## 3. Preparación del entorno

### 3.1 Variables mínimas requeridas

Crear un archivo `.env` con lo mínimo necesario:

```env
APP_ENV=development
APP_JWT_SECRET=tu_secret_muy_seguro
APP_COOKIE_SECURE=false
APP_CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/universidad
JWT_SECRET_KEY=tu_secret_muy_seguro
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 3.2 Levantar el backend

Desde la ruta del proyecto:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

En Windows PowerShell:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 3.3 URL base de la API

Por defecto:

```text
http://localhost:8000
```

### 3.4 Consideraciones por ambiente

- Dev: se permiten orígenes locales como `http://localhost:3000`.
- Prod: solo debe permitirse dominios explícitos y cookies con `Secure=true`.

### 3.5 Usuarios de prueba (obligatorio para login)

La API no trae usuarios al iniciar. `POST /users/` exige rol Administrador, así que el primer acceso se crea con el seed:

```powershell
cd backend
python -m scripts.seed_users
```

| Rol | Email | Contraseña |
| --- | --- | --- |
| Administrador | `admin@universidad.test` | `Secret123!` |
| Docente | `teacher@universidad.test` | `Secret123!` |
| Estudiante | `student@universidad.test` | `Secret123!` |

Detalle y flujo de login: `README.md` (sección *Usuarios de prueba*).

---

## 4. Autenticación y autorización

### 4.1 Login

#### Endpoint

```http
POST /auth/login
```

#### Headers

```http
Content-Type: application/json
```

#### Payload esperado

```json
{
  "email": "admin@universidad.test",
  "password": "Secret123!"
}
```

#### Respuesta esperada

```json
{
  "access_token": "<jwt>",
  "token_type": "bearer"
}
```

Además, el backend intenta guardar la cookie `access_token` con `HttpOnly`.

#### Código HTTP esperado

- `200 OK` si las credenciales son válidas.
- `401 Unauthorized` si el usuario no existe o la contraseña es incorrecta.

#### Errores comunes

- Email inválido: `422 Unprocessable Entity`
- Contraseña demasiado corta: `422 Unprocessable Entity`
- Usuario inactivo: `401 Unauthorized`

### 4.2 Uso del token

#### Opción A: Header Authorization

```http
Authorization: Bearer <jwt>
```

#### Opción B: Cookie

Cuando el navegador o cliente soporta cookies, el backend puede usar la cookie `access_token`.

#### Respuesta de error

```json
{
  "detail": "No se proporcionó un token de autenticación"
}
```

Código esperado:

- `401 Unauthorized`

### 4.3 Logout

#### Endpoint

```http
POST /auth/logout
```

#### Response esperada

```json
{
  "detail": "Sesión cerrada correctamente"
}
```

Código esperado:

- `200 OK`

---

## 5. Documentación por dominio

En todas las secciones siguientes, se usa este formato estándar:

- URL
- Método
- Roles permitidos
- Headers requeridos
- Request body
- Response exitosa
- Códigos HTTP esperados

---

## 5.1 Auth

### Login

#### URL

```http
POST /auth/login
```

#### Roles permitidos

- Público

#### Request JSON

```json
{
  "email": "admin@universidad.test",
  "password": "Secret123!"
}
```

#### Response exitosa

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Códigos esperados

- `200 OK`
- `401 Unauthorized`
- `422 Unprocessable Entity`

### Logout

#### URL

```http
POST /auth/logout
```

#### Roles permitidos

- Usuario autenticado

#### Response exitosa

```json
{
  "detail": "Sesión cerrada correctamente"
}
```

#### Códigos esperados

- `200 OK`

---

## 5.2 Usuarios

### Crear usuario

#### URL

```http
POST /users/
```

#### Roles permitidos

- Administrador

#### Headers

```http
Authorization: Bearer <jwt>
Content-Type: application/json
```

#### Request JSON

```json
{
  "email": "docente1@universidad.test",
  "full_name": "Ana García",
  "password": "Secret123!"
}
```

#### Response exitosa

```json
{
  "id": 2,
  "email": "docente1@universidad.test",
  "full_name": "Ana García",
  "is_active": true,
  "is_superuser": false,
  "roles": []
}
```

#### Códigos esperados

- `201 Created`
- `401 Unauthorized`
- `403 Forbidden` si no tiene rol.
- `409 Conflict` si el email ya existe.

### Listar usuarios

#### URL

```http
GET /users/
```

#### Roles permitidos

- Administrador
- Docente

#### Headers

```http
Authorization: Bearer <jwt>
```

#### Response exitosa

```json
[
  {
    "id": 1,
    "email": "admin@universidad.test",
    "full_name": "Admin Test",
    "is_active": true,
    "is_superuser": false,
    "roles": [
      {
        "id": 1,
        "name": "Administrador",
        "description": "Administrador del sistema"
      }
    ]
  }
]
```

#### Códigos esperados

- `200 OK`
- `401 Unauthorized`

### Actualizar usuario

#### URL

```http
PUT /users/{user_id}
```

#### Roles permitidos

- Administrador
- Docente

#### Request JSON

```json
{
  "full_name": "Ana García López",
  "is_active": true
}
```

#### Response exitosa

```json
{
  "id": 2,
  "email": "docente1@universidad.test",
  "full_name": "Ana García López",
  "is_active": true,
  "is_superuser": false,
  "roles": []
}
```

#### Códigos esperados

- `200 OK`
- `404 Not Found`
- `401 Unauthorized`

### Cambiar estado

#### URL

```http
PUT /users/{user_id}
```

#### Request JSON

```json
{
  "is_active": false
}
```

#### Códigos esperados

- `200 OK`
- `401 Unauthorized`
- `403 Forbidden` cuando el usuario no tiene permisos

---

## 5.3 Roles

### Crear rol

#### URL

```http
POST /roles/
```

#### Roles permitidos

- Administrador

#### Request JSON

```json
{
  "name": "Docente",
  "description": "Docente universitario"
}
```

#### Response exitosa

```json
{
  "id": 2,
  "name": "Docente",
  "description": "Docente universitario"
}
```

#### Códigos esperados

- `201 Created`
- `409 Conflict` si el nombre ya existe
- `401 Unauthorized`

### Listar roles

#### URL

```http
GET /roles/
```

#### Roles permitidos

- Administrador

#### Response exitosa

```json
[
  {
    "id": 1,
    "name": "Administrador",
    "description": "Administrador del sistema"
  }
]
```

#### Códigos esperados

- `200 OK`

---

## 5.4 Materias

### Crear materia

#### URL

```http
POST /subjects/
```

#### Roles permitidos

- Administrador
- Docente

#### Request JSON

```json
{
  "code": "MAT101",
  "name": "Matemáticas I",
  "credits": 4,
  "description": "Fundamentos de álgebra y cálculo"
}
```

#### Response exitosa

```json
{
  "id": 1,
  "code": "MAT101",
  "name": "Matemáticas I",
  "credits": 4,
  "description": "Fundamentos de álgebra y cálculo"
}
```

#### Códigos esperados

- `201 Created`
- `409 Conflict` si el código ya existe
- `401 Unauthorized`

### Listar materias

#### URL

```http
GET /subjects/
```

#### Roles permitidos

- Administrador
- Docente
- Estudiante

#### Response exitosa

```json
[
  {
    "id": 1,
    "code": "MAT101",
    "name": "Matemáticas I",
    "credits": 4,
    "description": "Fundamentos de álgebra y cálculo"
  }
]
```

#### Códigos esperados

- `200 OK`

### Actualizar materia

#### URL

```http
PUT /subjects/{subject_id}
```

#### Request JSON

```json
{
  "name": "Matemáticas I Avanzadas",
  "credits": 5
}
```

#### Response exitosa

```json
{
  "id": 1,
  "code": "MAT101",
  "name": "Matemáticas I Avanzadas",
  "credits": 5,
  "description": "Fundamentos de álgebra y cálculo"
}
```

#### Códigos esperados

- `200 OK`
- `404 Not Found`

### Desactivar materia

#### URL

```http
DELETE /subjects/{subject_id}
```

#### Roles permitidos

- Administrador

#### Códigos esperados

- `204 No Content`
- `404 Not Found`

---

## 5.5 Inscripciones

### Inscribir estudiante

#### URL

```http
POST /enrollments/
```

#### Roles permitidos

- Administrador
- Docente

#### Request JSON

```json
{
  "user_id": 3,
  "subject_id": 1,
  "period_id": 1,
  "status": "active"
}
```

#### Response exitosa

```json
{
  "id": 1,
  "user_id": 3,
  "subject_id": 1,
  "period_id": 1,
  "status": "active"
}
```

#### Códigos esperados

- `201 Created`
- `409 Conflict` si ya existe la inscripción para ese usuario, materia y período
- `404 Not Found` si no existen las entidades relacionadas

### Consultar inscripciones

#### URL

```http
GET /enrollments/
```

#### Roles permitidos

- Administrador
- Docente
- Estudiante (solo propias)

#### Response exitosa

```json
[
  {
    "id": 1,
    "user_id": 3,
    "subject_id": 1,
    "period_id": 1,
    "status": "active"
  }
]
```

#### Códigos esperados

- `200 OK`
- `401 Unauthorized`

### Cancelar inscripción

#### URL

```http
DELETE /enrollments/{enrollment_id}
```

#### Roles permitidos

- Administrador
- Docente
- Estudiante propietario

#### Códigos esperados

- `204 No Content`
- `404 Not Found`
- `403 Forbidden`

---

## 5.6 Calificaciones

### Registrar calificación

#### URL

```http
POST /grades/
```

#### Roles permitidos

- Administrador
- Docente

#### Request JSON

```json
{
  "enrollment_id": 1,
  "type": "Parcial",
  "score": 88.5,
  "comments": "Muy buen desempeño"
}
```

#### Response exitosa

```json
{
  "id": 1,
  "enrollment_id": 1,
  "type": "Parcial",
  "score": 88.5,
  "comments": "Muy buen desempeño"
}
```

#### Códigos esperados

- `201 Created`
- `404 Not Found`
- `401 Unauthorized`

### Consultar calificaciones

#### URL

```http
GET /grades/
```

#### Roles permitidos

- Administrador
- Docente
- Estudiante (solo propias)

#### Response exitosa

```json
[
  {
    "id": 1,
    "enrollment_id": 1,
    "type": "Parcial",
    "score": 88.5,
    "comments": "Muy buen desempeño"
  }
]
```

#### Códigos esperados

- `200 OK`
- `401 Unauthorized`
- `403 Forbidden`

### Actualizar calificación

#### URL

```http
PUT /grades/{grade_id}
```

#### Request JSON

```json
{
  "score": 92,
  "comments": "Excelente rendimiento final"
}
```

#### Response exitosa

```json
{
  "id": 1,
  "enrollment_id": 1,
  "type": "Parcial",
  "score": 92,
  "comments": "Excelente rendimiento final"
}
```

#### Códigos esperados

- `200 OK`
- `404 Not Found`
- `403 Forbidden`

---

## 6. Validación de roles y permisos

### Ejemplo 1: Acceso permitido

#### Request

```http
GET /subjects/
Authorization: Bearer <token_admin>
```

#### Resultado esperado

- `200 OK`

### Ejemplo 2: Acceso denegado por rol

#### Request

```http
POST /roles/
Authorization: Bearer <token_estudiante>
```

#### Resultado esperado

```json
{
  "detail": "No tiene permisos suficientes para acceder a este recurso"
}
```

Código esperado:

- `401 Unauthorized`

### Ejemplo 3: Acceso denegado por ownership

#### Request

```http
GET /users/2
Authorization: Bearer <token_estudiante_que_no_es_este_usuario>
```

#### Resultado esperado

```json
{
  "detail": "No tiene permisos para acceder a este recurso"
}
```

Código esperado:

- `401 Unauthorized`

---

## 7. Validación de errores comunes

### 400 Bad Request

Se usa cuando el payload no cumple reglas mínimas o hay datos inválidos.

```json
{
  "detail": "El email debe incluir un símbolo @ y un dominio válido"
}
```

### 401 Unauthorized

Cuando no hay token válido o el usuario está inactivo.

```json
{
  "detail": "Token inválido o expirado"
}
```

### 403 Forbidden

Cuando el usuario está autenticado pero no tiene permisos necesarios.

```json
{
  "detail": "No tiene permisos suficientes para acceder a este recurso"
}
```

### 404 Not Found

Cuando el recurso no existe.

```json
{
  "detail": "Usuario con id 99 no encontrado"
}
```

### 422 Unprocessable Entity

Cuando el payload tiene errores de validación de Pydantic.

```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "Value error, El email debe incluir un símbolo @ y un dominio válido",
      "type": "value_error"
    }
  ]
}
```

---

## 8. Uso de Swagger / OpenAPI

### Acceder a la documentación

Ejecutar:

```bash
uvicorn app.main:app --reload
```

Luego abrir:

```text
http://localhost:8000/docs
```

### Cómo probar endpoints desde Swagger

1. Abrir `/docs`.
2. Click en el endpoint deseado.
3. Completar los parámetros o body JSON.
4. Ejecutar “Try it out”.
5. Revisar request, response y códigos HTTP.

### Cómo interpretar schemas

- Models: definiciones del payload.
- Responses: estructuras esperadas.
- Validation: rechazo automático de entrada incorrecta.

---

## 9. Checklist de validación de API

Marca cada punto a medida que lo valides:

- [ ] El backend levanta correctamente.
- [ ] Login responde con `200 OK`.
- [ ] JWT se recibe y se usa correctamente.
- [ ] CRUD de usuarios funciona.
- [ ] CRUD de materias funciona.
- [ ] CRUD de inscripciones funciona.
- [ ] CRUD de calificaciones funciona.
- [ ] Roles restringen acceso correctamente.
- [ ] Ownership se valida correctamente.
- [ ] Respuestas 401/403/404/422 se entienden.
- [ ] No se exponen hashes ni datos sensibles.
- [ ] Swagger UI se puede usar para probar endpoints.

---

## 10. Conclusión

Las APIs del backend Universidad Digital están listas para validación manual mediante Swagger UI, Postman o cURL. La verificación principal debe centrarse en:

- autenticación,
- permisos por rol,
- ownership,
- manejo de errores,
- integridad de respuestas y seguridad básica.

Si se cumplen estas validaciones manuales, la API queda en un estado adecuado para pruebas con frontend y para preparación de despliegue productivo.
