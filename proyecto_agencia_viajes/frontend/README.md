# Itinera · frontend

MVP del CRM de agencia construido con React 18, TypeScript estricto y Vite 5.

## Desarrollo

```powershell
npm install
npm run dev
```

En desarrollo, las llamadas usan `/api` y Vite las reescribe hacia
`http://localhost:8000` (el proxy elimina el prefijo). La autenticación usa
exclusivamente la cookie `itinera_session`, marcada HttpOnly por el backend;
cada llamada usa `credentials: include` y la sesión se hidrata con
`GET /api/auth/me`. No se guarda ningún token en el navegador.
Las oportunidades muestran el `client_id` porque las respuestas actuales no
incluyen el nombre del cliente. Se añadió únicamente `GET /auth/me` y el
ajuste de cookie de sesión requerido para este frontend; el resto de rutas y
payloads siguen los esquemas existentes.

## Verificación

```powershell
npm run build
npm test
```
