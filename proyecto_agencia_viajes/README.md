# Itinera

Backend modular para el CRM de una agencia de viajes. Cada módulo mantiene sus modelos ORM, servicios, esquemas, puertos y rutas
directamente en su carpeta. Las excepciones base viven en `app/core` y las
excepciones específicas junto a cada módulo.

Los reportes son una excepción controlada: son consultas de solo lectura y
mantienen sus propios lectores SQL en `reports/repository.py`.

## Supuestos

- El identificador de las entidades es un entero autoincremental.
- La configuración usa `DATABASE_URL`; por defecto apunta a PostgreSQL local.
- La invalidación de sesión se representa con una respuesta exitosa; el JWT
  sigue siendo stateless.
- Alembic se configura en `backend/alembic.ini` y sus migraciones viven en
  `backend/migrations/`. `migrations/env.py` importa los modelos SQLAlchemy
  de cada `models.py` para construir el metadata utilizado por `alembic check`.

## Verificación

```powershell
python -m compileall -q app scripts
python -m pytest tests/architecture -q
python -m pytest -q
alembic check
```

Desde `backend/`, los comandos para preparar la base de datos y crear usuarios
son:

```powershell
python -m alembic upgrade head
python -m scripts.create_user admin "cambia-esta-clave"
python -m scripts.create_user agente "cambia-esta-otra-clave"
```

La conexión usada por Alembic se toma de `DATABASE_URL` en `.env`.

Para crear el usuario administrador de desarrollo mediante variables de
entorno, copia [.env.example](./backend/.env.example) a `.env`, cambia
`ADMIN_USERNAME` y `ADMIN_PASSWORD`, y ejecuta desde `backend/`:

```powershell
python -m alembic upgrade head
python -m scripts.create_user
```

También se pueden pasar el usuario y la contraseña como argumentos:

```powershell
python -m scripts.create_user admin "contraseña-de-desarrollo"
```
