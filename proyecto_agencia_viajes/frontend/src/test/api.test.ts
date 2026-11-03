import { describe, expect, it, vi } from 'vitest';
import { ApiError, request } from '../api/client';
describe('httpClient', () => {
  it('incluye cookies y normaliza errores de API', async () => {
    vi.stubGlobal('fetch', vi.fn(() => Promise.resolve(new Response(JSON.stringify({ code: 'BAD_INPUT', detail: 'Datos inválidos' }), { status: 422 }))));
    await expect(request('/clients')).rejects.toMatchObject({ status: 422, code: 'BAD_INPUT', message: 'Datos inválidos' });
    expect(fetch).toHaveBeenCalledWith('/api/clients', expect.objectContaining({ credentials: 'include' }));
  });
  it('lanza ApiError y notifica 401', async () => {
    const callback = vi.fn(); const { onUnauthorized } = await import('../api/client'); const cleanup = onUnauthorized(callback);
    vi.stubGlobal('fetch', vi.fn(() => Promise.resolve(new Response(JSON.stringify({ detail: 'No autorizado' }), { status: 401 }))));
    await expect(request('/auth/me')).rejects.toBeInstanceOf(ApiError); expect(callback).toHaveBeenCalledOnce(); cleanup();
  });
});
