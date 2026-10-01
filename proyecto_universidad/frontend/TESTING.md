# Estrategia de pruebas frontend — Universidad Digital

## Objetivo

La suite valida el **comportamiento observable** de la interfaz de tareas académicas.
No se inspecciona estado interno de React, ni funciones privadas, ni el DOM con
`querySelector`. El criterio es el mismo que usa un usuario: lo que puede ver,
leer con un lector de pantalla y hacer con teclado o ratón.

> Mientras más se parezca al uso real del usuario, más confiable es el test.

## Pirámide de pruebas en este frontend

| Capa | Carpeta | Qué demuestra | Qué no debe hacer |
| --- | --- | --- | --- |
| Unitarias de comportamiento | `src/tests/unit/` | Render inicial, roles, labels y props visibles | Simular clicks ni afirmar implementación |
| Interacción | `src/tests/interaction/` | `userEvent`: escribir, Tab, Enter, Space, click | Comprobar estilos o datos de servidor |
| Funcionales de UI | `src/tests/functional/` | La interfaz cambia después de la acción | Duplicar cada click ya cubierto arriba |

Una prueba no cambia de nivel por su nombre, sino por su dependencia: si habla
con un servicio simulado o combina formulario y lista, es funcional.

## Estructura

```text
frontend/src/
├── components/          # TaskForm, TaskList y TaskBoard (código de producto)
└── tests/
    ├── setup/           # arranque de Vitest, matchers y render con userEvent
    ├── unit/            # comportamiento aislado, sin clics
    ├── interaction/     # acciones realistas del usuario
    ├── functional/      # cambios de UI y datos de servidor simulados
    └── fixtures/        # tareas de ejemplo, reutilizables y deterministas
```

### Propósito de cada carpeta de tests

- **setup/**: deja el entorno listo una sola vez. Aquí viven jsdom matchers y
  el helper `renderWithUser`, para no repetir `userEvent.setup()` a mano.
- **unit/**: responde “¿qué ve una persona al abrir el componente?”. Roles,
  textos, labels y estados vacíos.
- **interaction/**: responde “¿el usuario puede hacer la acción?”. Siempre usa
  `userEvent` y `await`.
- **functional/**: responde “¿la pantalla reacciona bien?”. Errores, limpieza
  del input, botón deshabilitado, lista que se actualiza, mocks de servidor.
- **fixtures/**: datos de prueba con nombres de dominio (`pendingTask`), no
  objetos anónimos copiados en cada archivo.

## Archivos de configuración

### `vite.config.ts`

Vitest se monta sobre Vite. El bloque `test` define:

- **environment: jsdom** — simula `document` y `window` sin abrir un navegador.
- **setupFiles** — carga `vitest.setup.ts` antes de cada archivo de prueba.
- **include** — solo ejecuta `src/tests/**/*.test.{ts,tsx}`.
- **css: true** — permite aserciones de clase CSS usadas como contrato visual.
- **pool: threads**, un worker y `isolate: false` — evita cuelgues del pool
  `forks` en Windows cuando la ruta del proyecto contiene espacios, y reutiliza
  el entorno jsdom entre archivos para no esperar ~10 s de arranque por test file.
- **coverage** — mide los componentes y el servicio de tareas, no páginas
  enteras ajenas a este modelo.

### `src/tests/setup/vitest.setup.ts`

Importa `@testing-library/jest-dom/vitest` y ejecuta `cleanup()` después de
cada prueba. Los matchers cubren interfaz (`toBeInTheDocument`, `toBeChecked`,
`toBeDisabled`, `toHaveClass`, `toHaveValue`). El cleanup evita que un árbol
React quede colgado en jsdom y ensucie la siguiente prueba.

### `src/tests/setup/test-utils.ts`

`renderWithUser` combina Arrange de Testing Library con un `userEvent.setup()`
nuevo por prueba. Cada test queda aislado: no comparte buffer de teclado ni
foco con el anterior.

### `tsconfig.app.json`

Declara tipos de `vitest/globals` y de Testing Library para que el editor
reconozca `expect(...).toBeInTheDocument()`.

## Cómo se eligen las queries

Orden obligatorio, el mismo que recomienda Testing Library:

1. `getByRole` — botones, inputs, listas, formularios, alerts.
2. `getByLabelText` — confirma que el `<label htmlFor>` está bien asociado.
3. `getByText` — mensajes visibles sin rol semántico propio.
4. `testId` — no se usa en esta suite. Si hiciera falta, sería un olor de
   accesibilidad en el componente, no una solución del test.

`screen` sustituye a `container`. El test pregunta por lo que hay en la
página, no por un nodo HTML interno.

## Mocks: cuándo `vi.fn()` y cuándo `vi.mock()`

### `vi.fn()` — un callback o una función suelta

Úsalo cuando el componente recibe la dependencia por **props**:

```ts
const onCreateTask = vi.fn();
render(<TaskForm onCreateTask={onCreateTask} />);
```

Sirve para `onCreateTask`, `onToggle` y `onDelete`. También para simular
asincronía sin un módulo:

```ts
const onCreateTask = vi.fn(() => new Promise<void>((resolve) => { /* ... */ }));
```

No sustituye un archivo: solo espias el contrato público del componente.

### `vi.mock()` — un módulo completo

Úsalo cuando el componente **importa** una dependencia (API, servicio, router):

```ts
vi.mock('@/services/taskService', () => ({
  fetchTasks: vi.fn(),
  createTask: vi.fn(),
  toggleTask: vi.fn(),
  deleteTask: vi.fn(),
}));
```

Eso evita red real y estado compartido del store en memoria. Se configura en
`beforeEach` con `mockResolvedValue` / `mockRejectedValue` para datos de
servidor simulados.

Regla práctica: si puedes pasarlo por props, `vi.fn()`. Si nace de un import,
`vi.mock()`.

## Convenciones

- Nombre en español, como historia: `muestra un error accesible cuando el título está vacío`.
- Patrón AAA: Arrange (render + mocks), Act (una interacción), Assert (lo observable).
- Cada prueba construye su propio árbol. No reutilices un `render` entre casos.
- `await` en cada `userEvent` y en `findBy` / `waitFor`.
- No se prueba el setter de `useState` ni el recuento interno de caracteres
  salvo que el usuario lo vea.
- Evita over-testing: un click no necesita tres archivos que afirmen lo mismo.
  Unit afirma presencia, interaction afirma la acción, functional afirma el
  efecto en pantalla.

## Casos cubiertos

### TaskForm

- input vacío
- texto válido
- texto largo (más de 120 caracteres, pegado como haría un usuario)
- espacios en blanco
- múltiples envíos
- limpieza del campo
- submit con Enter
- navegación con Tab
- botón deshabilitado durante una promesa
- error si el callback asíncrono falla

### TaskList

- lista vacía
- múltiples tareas
- toggle completado (click, Space y re-render)
- eliminación (click y Enter)
- renderización condicional lista / estado vacío

### TaskBoard

- la tarea creada aparece en la lista
- el estilo de completada cambia de verdad, no solo el callback
- datos de servidor simulados con `vi.mock`
- error de carga

## Ejecución

```powershell
cd frontend
npm install
npm test
npm run test:watch
npm run test:coverage
```

Vitest usa jsdom. No hace falta que el backend esté en marcha.

## Uso de IA como copiloto

La IA acelera, pero no sustituye el criterio de comportamiento. Pídele que
piense como usuario, no como inspector del código fuente.

### Generar casos faltantes

```text
Eres un Frontend Test Engineer. Lee TaskForm.tsx y src/tests/**/TaskForm.test.tsx.
Propón casos de comportamiento que aún no existan. No uses testId ni querySelector.
Prioriza getByRole y userEvent. Devuelve solo nombres de prueba y el Arrange-Act-Assert.
```

### Detectar huecos de cobertura

```text
Compara la cobertura de vitest con los flujos reales: vacío, válido, largo,
espacios, Enter, Tab, error de red y doble envío. Lista huecos de comportamiento,
no líneas de código sin cubrir. No sugieras tests de snapshot.
```

### Simplificar tests largos

```text
Refactoriza este test para que tenga una sola conducta. Extrae datos a fixtures.
Mantén userEvent y screen. No añadas expect sobre implementación.
```

### Reducir duplicación

```text
Estos tres tests repiten el mismo render. Extrae un helper renderWithUser y
fixtures de tareas. No crees un beforeEach que oculte el Arrange de cada caso
si el dato importante cambia.
```

### Qué no pedir a la IA

- “Cubre el 100% de líneas” — produce tests frágiles.
- “Usa container.firstChild” — rompe la regla de usuario.
- “Mockea React.useState” — prueba implementación, no producto.

## Resultado esperado

Un estudiante puede abrir `TaskForm` y `TaskList`, ejecutar `npm test` y ver
una suite alineada con un equipo React profesional: accesible, independiente,
legible como historias de usuario y con mocks solo en la frontera real.
