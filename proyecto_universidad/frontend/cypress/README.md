# Suite E2E Cypress — Universidad Digital

Pruebas end-to-end del flujo real:

`login → navegación → creación de tarea → confirmación → persistencia → visualización`

Cada caso combina **UI + API + datos**: status HTTP, cuerpo JSON, tiempo de respuesta y consistencia de lo renderizado. No hay `cy.wait(5000)`.

## Arquitectura

```text
frontend/cypress/
├── e2e/
│   ├── auth/login.cy.ts
│   ├── navigation/dashboard-access.cy.ts
│   ├── tasks/create-task.cy.ts
│   ├── tasks/confirmation.cy.ts
│   ├── tasks/visualization.cy.ts
│   ├── resilience/backend-failures.cy.ts
│   └── journeys/academic-task-flow.cy.ts
├── pages/                 # Page Objects
├── helpers/               # env, JWT de prueba, factories, aserciones
├── fixtures/              # usuarios, tareas y errores
└── support/
    ├── e2e.ts             # hooks globales y health-check
    ├── intercepts.ts      # spies y stubs de red
    └── commands/          # login, API y tareas
```

## Prerrequisitos

1. Backend en `http://127.0.0.1:8000`
2. Frontend en `http://localhost:3000`
3. Usuarios semilla (admin, docente, estudiante)

### 1. Semilla de usuarios E2E

```powershell
cd backend
python -m scripts.seed_e2e
```

Credenciales (solo entorno de prueba):

| Rol | Email | Password |
| --- | --- | --- |
| Estudiante | `student@universidad.test` | `Secret123!` |
| Administrador | `admin@universidad.test` | `Secret123!` |
| Docente | `teacher@universidad.test` | `Secret123!` |

### 2. Arrancar la API

```powershell
cd backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 3. Arrancar la SPA

```powershell
cd frontend
npm install
npm run dev
```

### 4. Variables de entorno

Copia `frontend/cypress.env.example.json` a `frontend/cypress.env.json` si necesitas override local. Por defecto:

- `baseUrl`: `http://localhost:3000`
- `apiUrl`: `http://127.0.0.1:8000`

## Ejecución

```powershell
cd frontend
npm run test:e2e:open     # modo interactivo
npm run test:e2e          # headless CI
npm run test:e2e:headed   # headed Chrome
```

Un spec concreto:

```powershell
npx cypress run --spec cypress/e2e/journeys/academic-task-flow.cy.ts
```

Ambiente distinto:

```powershell
$env:CYPRESS_baseUrl="http://localhost:3000"
$env:CYPRESS_apiUrl="http://127.0.0.1:8000"
npm run test:e2e
```

## Qué cubre la suite

| Área | Casos |
| --- | --- |
| Autenticación | login válido, inválido, vacío, token expirado, backend caído |
| Navegación | dashboard autenticado, bloqueo anónimo, RBAC estudiante→admin |
| Creación | válida, inválida, HTTP 500, backend lento, sin conexión |
| Confirmación | UI + GET por id + listado persistido |
| Visualización | datos correctos y refresco con sesión |
| Resiliencia | JSON corrupto, timeout 504, validación inconsistente, respuesta parcial |

## Convenciones

- Comandos personalizados en `support/commands/`
- Intercepts con alias; se espera la petición, no un reloj
- Las tareas de prueba usan el prefijo `e2e-tarea-` y se borran al terminar
- `cy.session` cachea el login de UI; el token vive en `sessionStorage`, no en `localStorage`
- Credenciales salen de fixtures/`cypress.env`, nunca de código de producto
