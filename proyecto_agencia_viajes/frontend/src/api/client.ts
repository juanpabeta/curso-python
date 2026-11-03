const API = '/api';
export class ApiError extends Error {
  constructor(public readonly status: number, public readonly code: string, message: string) { super(message); this.name = 'ApiError'; }
}
let unauthorized: (() => void) | undefined;
export function onUnauthorized(callback: () => void) { unauthorized = callback; return () => { unauthorized = undefined; }; }
export async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  let response: Response;
  try {
    response = await fetch(`${API}${path}`, { credentials: 'include', ...init, headers: { ...(init.body ? { 'Content-Type': 'application/json' } : {}), ...init.headers } });
  } catch {
    throw new ApiError(0, 'NETWORK_ERROR', 'No hay conexión con el servidor');
  }
  if (!response.ok) {
    let payload: { detail?: string; code?: string } = {};
    try { payload = await response.json(); } catch { /* non-json error */ }
    if (response.status === 401) unauthorized?.();
    throw new ApiError(response.status, payload.code ?? (response.status === 401 ? 'UNAUTHORIZED' : 'API_ERROR'), payload.detail ?? 'No se pudo completar la solicitud');
  }
  return response.status === 204 ? undefined as T : response.json();
}
