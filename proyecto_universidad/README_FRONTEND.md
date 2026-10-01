# Frontend Universidad Digital

Aplicación web del sistema académico. Se adapta a la API FastAPI existente: no duplica sus reglas de negocio y no modifica el backend. El servidor sigue siendo la fuente de verdad para autenticación, unicidad, existencia de registros y autorización de los endpoints que ya la exigen.

## 1. Arquitectura

React 18, TypeScript estricto y Vite. El estado de sesión vive en un contexto (patrón Flux: una acción de login/logout actualiza un único estado y la interfaz se deriva de él). Los datos académicos no se guardan en un store global: cada vista los pide a través de un hook, el hook llama a un servicio y el servicio usa el cliente Axios.

Separación aplicada:

| Capa | Responsabilidad |
| --- | --- |
| `components/` | UI reutilizable. Sin reglas académicas ni llamadas HTTP. |
| `pages/` | Un caso de uso por vista: formulario, tabla y acciones. |
| `hooks/` | Estado de carga, error y recarga. |
| `services/` | Contratos HTTP y comprobación mínima de la forma de la respuesta. |
| `utils/` | Validación de UX, sanitización y mensajes seguros. |
| `auth/` y `context/` | Sesión, guardas y redirección por rol. |
| `routes/` | Rutas públicas y protegidas. |

La validación del formulario evita envíos vacíos o fuera de rango. Si el servidor rechaza el dato, se muestra su mensaje de dominio (por ejemplo un duplicado) y no se inventa otra regla.

## 2. Estructura de carpetas

```text
frontend/
├── src/
│   ├── api/            # Axios, interceptores y rutas de la API
│   ├── auth/           # Guardas y sesión de pestaña
│   ├── components/     # UI (botón, campos, tabla, modal, alerta) y tareas
│   ├── context/        # AuthContext
│   ├── hooks/          # useAuth, useFetch, useSubjects, useEnrollments, useGrades
│   ├── layouts/        # Auth y dashboard
│   ├── pages/          # Login, paneles, CRUD y errores
│   ├── routes/         # Rutas y menú por rol
│   ├── services/       # Materias, períodos, usuarios, inscripciones, calificaciones, tareas
│   ├── styles/         # Estilos globales
│   ├── utils/          # Validación, sanitización, errores y vista académica
│   └── main.tsx
├── .env.example
└── package.json
```

## 3. Flujo de autenticación

1. El usuario envía correo y contraseña en `/login`.
2. El cliente llama a `POST /auth/login` con `withCredentials`.
3. El backend devuelve `access_token` y, además, escribe la cookie HttpOnly `access_token`.
4. El token de la respuesta queda en memoria y se copia a `sessionStorage` solo durante la vida de la pestaña. No se usa `localStorage`.
5. El interceptor añade `Authorization: Bearer <token>` en cada petición.
6. `GET /auth/me` restaura nombre, correo y roles. Si falla, la sesión se descarta.
7. Un `401` distinto del login limpia la sesión y devuelve al usuario a `/login` con un aviso de sesión expirada.
8. `POST /auth/logout` borra la cookie en el servidor y el cliente olvida el token.

La cookie HttpOnly sigue activa porque el backend la emite. En desarrollo el frontend (`localhost:3000`) y la API (`127.0.0.1:8000`) son orígenes distintos, y la cookie `SameSite=Lax` no viaja en ese XHR. Por eso la pestaña también conserva el JWT para el encabezado `Authorization`. Las pruebas E2E existentes comprueban esa clave de `sessionStorage`.

## 4. Rutas

Públicas:

- `/login`
- `/unauthorized`
- `/404`
- `/error`

Protegidas por sesión y rol:

| Ruta | Rol |
| --- | --- |
| `/student` | Estudiante |
| `/teacher` y `/teacher/calificaciones` | Docente |
| `/admin`, `/admin/materias`, `/admin/usuarios`, `/admin/periodos`, `/admin/inscripciones`, `/admin/calificaciones` | Administrador |

`/` redirige al panel del rol. Un rol incorrecto va a `/unauthorized`. Una ruta desconocida va a `/404`. Un error de render no controlado muestra `/error` sin el stack.

## 5. Paneles

**Estudiante.** Materias inscritas, calificaciones, estado académico e inscripción. Solo se pintan inscripciones y notas cuyo `user_id` es el de la sesión. El estado (`Sin matrícula`, `En curso`, `Completado`, `Cerrado`) es un resumen visual de `enrollment.status` y de los créditos; no es una regla nueva del dominio.

**Docente.** Catálogo, inscripciones y registro o corrección de calificaciones. La API no asocia una materia a un docente, así que el panel opera sobre el catálogo que el backend devuelve.

**Administrador.** CRUD de materias, usuarios, períodos, inscripciones y calificaciones. Al crear un usuario se llama a `POST /users/` y después a `POST /users/{id}/roles/{role_id}`, porque el alta de usuario no recibe el rol en el mismo cuerpo. La API no permite quitar un rol ya asignado. El indicador `is_superuser` no se edita desde la interfaz para no elevar privilegios por accidente.

Las tareas académicas (`/tasks`) siguen en los tres paneles de inicio.

## 6. Seguridad aplicada

- Autenticación real contra `/auth/login`, `/auth/me` y `/auth/logout`.
- JWT fuera de `localStorage`. Memoria de la pestaña más `sessionStorage`, y cookie HttpOnly cuando el navegador la envía.
- Axios centraliza el token, el `401` y el rechazo de la promesa.
- Rutas protegidas por autenticación y por rol antes de montar la vista.
- El estudiante no llama a `/users` ni a `/roles`. Esos endpoints responden `401` si el rol no alcanza, y ese `401` cerraría la sesión.
- Las cadenas se sanitizan al enviar (se quitan etiquetas y espacios sobrantes). React escapa el texto al pintarlo. No hay `dangerouslySetInnerHTML`.
- Un `500`, un traceback o un mensaje con `password_hash` / `sqlalchemy` se sustituye por un texto genérico.
- Los errores de validación de FastAPI (`422`) y los mensajes de dominio (`404`, `409`) sí se muestran, porque son el contrato público.
- `esbuild` elimina `console` y `debugger` en el build de producción.
- La URL de la API sale de `VITE_API_BASE_URL`.

Alineación con las guías de frontend de OWASP: no se persiste el token en almacenamiento permanente, las entradas se tratan como texto, los errores no filtran internals y la autorización de la interfaz no reemplaza la del servidor.

## 7. Accesibilidad (WCAG 2.1 AA)

Decisiones:

- `lang="es"` en el documento y título por vista (`2.4.2`).
- Un `h1` en el panel (“Universidad Digital”) y `h2`/`h3` en cada caso de uso.
- Enlace “Saltar al contenido” como primer control enfocable.
- Cada control de formulario tiene `label` asociado, `aria-invalid` y `aria-describedby`.
- El primer campo inválido recibe el foco. El resumen de error de los formularios de gestión usa `role="alert"`.
- Login anuncia el error con `role="alert"`.
- Tablas con `caption` y `th scope="col"`.
- Modal con `role="dialog"`, `aria-modal`, foco inicial, ciclo de Tab, Escape y devolución del foco.
- Botones de al menos 44 px. Foco visible (`outline` azul `#174ea6`).
- Contraste revisado sobre la paleta: texto `#1a2433` y secundario `#52606d` sobre blanco (el secundario queda alrededor de 6.4:1), texto blanco sobre `#174ea6`, texto de error `#7a1b14` sobre fondo claro.
- `prefers-reduced-motion` anula animaciones.

Limitaciones conocidas:

- En el inicio del estudiante, docente y administrador el tablero de tareas ya usa el único `role="alert"` y el único `role="status"`. Los mensajes académicos de esas tres pantallas son texto visible y, en la inscripción, quedan asociados al formulario con `aria-describedby`. Así no se duplica el aviso que las pruebas E2E localizan por rol. En las pantallas de gestión el aviso sí usa `role="alert"` o `role="status"`.
- No hay un escáner automático (axe) en la integración continua. La revisión de contraste es de paleta, no un informe certificado píxel a píxel.
- El foco del modal está implementado en el componente, no con una librería de focus-trap.
- El riesgo principal de exclusión no es visual: un estudiante que dependa solo del teclado puede completar login, menú, tablas y formularios. Quien use lector de pantalla en el inicio oirá el error académico al llegar al texto, no como una alerta independiente, por la limitación anterior.

## 8. Variables de entorno

Frontend (`frontend/.env`, plantilla en `frontend/.env.example`):

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

No hay secretos en el frontend. La clave JWT pertenece solo al backend.

Backend de desarrollo, como referencia:

```env
APP_ENV=development
APP_COOKIE_SECURE=false
APP_CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
JWT_SECRET_KEY=cambiar-este-secreto
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

En producción `APP_COOKIE_SECURE` debe ser `true` y el origen de CORS debe ser el del frontend real.

## 9. Cómo ejecutar

Backend, desde `backend/`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
python -m scripts.seed_users
```

Frontend, desde `frontend/`:

```powershell
npm install
npm run dev
```

- Frontend: http://localhost:3000
- API: http://127.0.0.1:8000
- Swagger: http://127.0.0.1:8000/docs

Cuentas de desarrollo (también documentadas en `backend/README.md`):

| Rol | Correo | Contraseña |
| --- | --- | --- |
| Administrador | `admin@universidad.test` | `Secret123!` |
| Docente | `teacher@universidad.test` | `Secret123!` |
| Estudiante | `student@universidad.test` | `Secret123!` |

El login de desarrollo trae rellenas las credenciales de administrador. Son cuentas locales, no de producción.

Comprobaciones:

```powershell
cd frontend
npx tsc -b
npm test
```

`npx tsc -b` termina sin errores. `npm test` ejecuta Vitest (39 pruebas en la última corrida con el pool `forks`, incluidas tareas y contratos académicos). El pool `threads` configurado en Vite puede agotar el arranque del worker en esta máquina; el detalle del modelo de pruebas de tareas está en `frontend/TESTING.md`.

Build de producción:

```powershell
npm run build
```

## 10. Conexión con el backend

Cliente: `src/api/client.ts`. Rutas: `src/api/endpoints.ts`.

| Uso | Método y ruta |
| --- | --- |
| Sesión | `POST /auth/login`, `GET /auth/me`, `POST /auth/logout` |
| Materias | `GET/POST /subjects/`, `PUT/DELETE /subjects/{id}` |
| Períodos | `GET/POST /periods/`, `PUT/DELETE /periods/{id}` |
| Usuarios y roles | `GET/POST /users/`, `PUT/DELETE /users/{id}`, `GET /roles/`, `POST /users/{id}/roles/{role_id}` |
| Inscripciones | `GET/POST /enrollments/`, `PUT/DELETE /enrollments/{id}` |
| Calificaciones | `GET/POST /grades/`, `PUT/DELETE /grades/{id}` |
| Tareas | `GET/POST /tasks/`, `POST /tasks/{id}/toggle`, `DELETE /tasks/{id}` |

Estados de inscripción que la interfaz ofrece, y que el backend ya usa en sus pruebas: `active`, `completed`, `withdrawn`. Tipos de nota ofrecidos: Parcial, Final, Taller, Quiz y Proyecto. El servidor acepta cualquier tipo de 2 a 50 caracteres; si llega otro, el formulario de edición lo conserva.

## 11. Resultados de la auditoría

### Calidad

- SoC: la UI no decide si un correo existe ni si una inscripción está duplicada; eso lo responde la API.
- SRP: cada servicio habla con un recurso. Cada página cubre un caso de uso.
- DRY: cliente HTTP, `useFetch`, tabla, modal, campos y el mapeo de inscripciones se comparten. Los formularios de alta y edición viven en su página porque los campos no son idénticos.
- Tipado estricto (`strict`, `noUnusedLocals`). Las respuestas se comprueban antes de pintarlas.
- El CRUD administrativo repite el ciclo abrir modal / validar / guardar. Extraerlo más no cambia el comportamiento y se dejó explícito.

### Seguridad

- Sesión, guardas y mensajes revisados como se describe en la sección 6.
- Hallazgo residual, sin cambio de backend: `GET /enrollments/`, `GET /grades/`, `GET /subjects/` y `GET /periods/` no exigen rol. El estudiante filtra lo que ve, pero el navegador recibe la colección completa. Un cliente distinto puede leerla. La corrección de fondo es filtrar en la API.
- Hallazgo residual: el JWT de pestaña es legible por script si hubiera un XSS. La cookie HttpOnly mitiga el robo cuando el navegador la usa; el encabezado `Authorization` existe por el origen cruzado de desarrollo.
- No se expone `is_superuser` ni hashes. No se puede borrar la propia cuenta desde la tabla.

### Accesibilidad

Checklist WCAG 2.1 AA revisado en código: texto alternativo no aplica a iconos (los botones tienen nombre), teclado en controles nativos, foco visible, etiquetas, errores identificados, nombre y rol en diálogo y tabla, idioma de la página, jerarquía de encabezados, contraste de la paleta y objetivo táctil de 44 px en los botones nuevos.

Riesgo de exclusión documentado en la sección 7: el inicio comparte la región de alerta con el tablero de tareas.

### UX técnica

- Flujos de alta, edición, baja y reintento están en cada CRUD.
- Los números de los paneles salen de la API, no de datos fijos.
- Un error de red dice que no hay conexión. Un `500` no muestra la excepción.
- Misma paleta, mismos botones y mismas tablas en los tres roles.

### Qué se ajustó tras la revisión

- Los paneles dejaron de mostrar cifras de ejemplo.
- El estudiante ya no consulta endpoints que le cierran la sesión.
- Los errores `500` dejan de enseñar detalles internos.
- Los listados vacíos no aparecen mientras la primera carga sigue en curso.
- Las tres portadas pueden reintentar si la API no responde.
- Se añadió la página de error no controlado y el enlace para saltar al contenido.

## 12. Resultado

El frontend queda integrado a los contratos actuales, con autenticación real, paneles por rol, formularios validados y una auditoría escrita de lo que cumple y de lo que el backend aún deja abierto. Está listo para pruebas de usuario y para la revisión académica sin cambiar el servidor.
