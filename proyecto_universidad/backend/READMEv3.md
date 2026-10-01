# Universidad Digital – Backend Productivo

## 1. Propósito

El backend de Universidad Digital está preparado para ambientes de desarrollo y producción, con autenticación segura, control de acceso por roles, protección por ownership y configuración centralizada por entorno.

## 2. Perfiles de entorno

El proyecto distingue dos perfiles:

- development: restricciones relajadas para trabajo local
- production: configuración más estricta, cookies seguras y orígenes permitidos explícitos

### Variables recomendadas

```env
APP_ENV=production
APP_JWT_SECRET=tu_secret_muy_seguro
APP_COOKIE_SECURE=true
APP_CORS_ORIGINS=https://frontend-produccion.com
DATABASE_URL=postgresql://usuario:password@host:5432/universidad
JWT_SECRET_KEY=tu_secret_muy_seguro
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## 3. Configuración segura

- Variables de entorno centralizadas en app/core/config.py
- Uso de python-dotenv
- No se hardcodean secretos ni credenciales
- CORS dinámico según ambiente
- Cookies HttpOnly para la sesión
- Secure solo habilitado en producción

## 4. Seguridad aplicada

### JWT

- Emisión de access token firmado
- Validación de expiración y firma
- Uso de Authorization header y cookie fallback

### Autorización por rol

Roles soportados:

- Administrador
- Docente
- Estudiante

### Ownership

La aplicación valida si un usuario puede acceder a recursos propios o si tiene un rol que legitimiza la acción. Este patrón evita que un usuario manipule información ajena.

## 5. Flujo de autenticación

1. El cliente envía email y password al endpoint /auth/login.
2. El backend valida credenciales y estado del usuario.
3. Se emite un JWT y se guarda en cookie HttpOnly.
4. Cada ruta protegida valida el token con una dependencia.
5. Se aplica control por rol y ownership antes de ejecutar la lógica de negocio.

## 6. Estructura del proyecto

```text
backend/
├── app/
│   ├── auth/
│   ├── core/
│   ├── enrollments/
│   ├── grades/
│   ├── subjects/
│   ├── users/
│   ├── __init__.py
│   └── main.py
├── .env
├── README.md
├── READMEv2.md
├── READMEv3.md
├── requirements.txt
└── tests/
    └── test_auth_flow.py
```

## 7. Endpoints principales

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

### Calificaciones

- GET /grades/
- GET /grades/{grade_id}
- POST /grades/
- PUT /grades/{grade_id}
- DELETE /grades/{grade_id}

## 8. Recomendaciones de despliegue

- Ejecutar en entorno Linux con usuario no privilegiado
- Usar PostgreSQL real en producción
- Configurar HTTPS y cookies secure
- Restringir CORS a dominios autorizados
- Rotar secretos y usar secretos de entorno del host o plataforma
- Activar logs estructurados y monitoreo

## 9. Criterios de seguridad OWASP

- Autenticación y sesión protegidas
- Validación estricta de entrada
- Control de acceso basado en roles y ownership
- Protección de secretos en variables de entorno
- Evitación de exposición de datos sensibles
- Configuración segura por entorno

## 10. Estado del proyecto

El backend queda preparado para usos productivos y para pruebas con frontend, con una base sólida de seguridad y escalabilidad.
