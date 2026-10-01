# Estrategia de pruebas — Universidad Digital

## Objetivo y alcance real

La suite aplica una pirámide de pruebas sobre los dominios implementados:
autenticación, usuarios, roles, materias, periodos, matrículas y calificaciones.
El código actual no implementa pagos, reportes ni certificados. Sus expectativas
se documentan como contratos `xfail` estrictos: no producen falsos positivos y
se convertirán en pruebas E2E reales cuando existan esas capacidades.

## Estructura

```text
tests/
├── unit/          # lógica pura; Session, hashes y emisión de tokens simulados
├── integration/   # servicios/API conectados a SQLite temporal real
├── e2e/           # recorridos completos por HTTP, sin mocks internos
├── fixtures/      # ciclo de vida de BD, sesiones, clientes y autenticación
├── factories/     # builders deterministas con valores válidos y overrides
└── data/          # seeds declarativos, versionados y reproducibles
```

La mayor cantidad debe ser unitaria, seguida por integración y una capa E2E
pequeña. Una prueba no cambia de nivel por su nombre sino por sus dependencias.

## Convenciones

- Nombre: `test_<acción>_<resultado>[_cuando_<condición>]`.
- Patrón AAA: preparar (Arrange), ejecutar una sola conducta (Act) y comprobar
  resultados observables (Assert).
- Cada prueba recibe una base nueva: no depende del orden ni comparte estado.
- No se usa la fecha actual, red, archivos de usuario o PostgreSQL local.
- Los límites se parametrizan (`0`, máximos, negativos, `None`, tipos erróneos).
- `MagicMock` se usa solo en unitarias y en el punto donde vive la dependencia.
- `monkeypatch` reemplaza hashes/tokens/configuración de forma reversible.
- Las factories tienen defaults legibles; un test modifica únicamente el dato
  importante mediante overrides.

## Fixtures y scopes

Todas las fixtures mutables son `function`:

- `valid_user` / `invalid_user`: payloads didácticos.
- `course`, `academic_period`, `enrollment`: entidades persistidas.
- `db_engine` / `db_session`: SQLite en memoria con foreign keys habilitadas.
- `api_client`: API real con solo la conexión de BD sustituida.
- `simulated_auth_client`: autenticación simulada para aislar tests de rutas.
- `auth_headers`: login y JWT reales; se usa en integración/E2E.

`module` puede servir para datos inmutables costosos, pero no para una sesión
SQLAlchemy compartida. `session` es apropiado para iniciar una imagen de
contenedor una sola vez; cada prueba aún debe usar transacción o esquema
aislado. Elegir un scope mayor solo por velocidad introduce pruebas frágiles.

## Datos de prueba

Los datos viven en factories o `tests/data`, no dispersos en aserciones. El
seed declarado (`20260914`) permite configurar Faker en el futuro con
`Faker.seed(seed)`. No deben usarse datos personales reales. La aleatoriedad sin
seed, UUIDs innecesarios y timestamps actuales dificultan reproducir fallos.

## Seguridad

La suite cubre tokens ausentes/manipulados, usuarios inactivos, filtrado de
campos sensibles, validación de entrada y una cadena tipo SQL injection. Esto
no sustituye análisis SAST, revisión OWASP, pruebas de rate limiting ni un
pentest. Actualmente varias rutas académicas carecen de autorización; esa es
una brecha del producto, no algo que una fixture de test deba ocultar.

## Ejecución

```powershell
cd backend
python -m pip install -r requirements-test.txt
pytest
pytest -m unit
pytest -m integration
pytest -m e2e
pytest -m "security"
pytest --cov-report=html
```

`pytest.ini` registra markers de forma estricta y ejecuta cobertura de ramas.
`.coveragerc` mide código de aplicación. El build falla por debajo de 85%.

La meta no significa probar getters triviales solo para aumentar el número.
Debe cubrir decisiones de negocio, validación, autorización, errores, límites
y regresiones. Se excluyen únicamente archivos `__init__`, ramas imposibles de
tipado y código deliberadamente abstracto. No se excluyen rutas o servicios
difíciles: eso maquillaría el riesgo.

## CI

El workflow del repositorio:

1. prepara una versión soportada de Python;
2. instala dependencias bloqueadas por rangos;
3. ejecuta `ruff check app tests`;
4. ejecuta toda la suite con SQLite;
5. exige 85% de cobertura de ramas;
6. publica `coverage.xml` incluso cuando el job falla.

## Evolución recomendada

1. Implementar autorización/ownership en materias, matrículas y calificaciones.
2. Diseñar pagos con un puerto de gateway; mock del puerto en unitarias y
   sandbox/contenedor en integración.
3. Generar certificados desde una regla de aprobación y pago confirmado.
4. Implementar reportes como consultas/read models testeables.
5. Cambiar los tres contratos `xfail` a flujos E2E normales.
6. Añadir PostgreSQL con Testcontainers como job complementario; SQLite es
   rápido, pero no detecta todas las diferencias de tipos, locks y SQL.
