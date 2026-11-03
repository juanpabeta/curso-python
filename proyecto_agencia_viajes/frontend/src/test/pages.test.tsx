import { render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { ClientsPage, LoginPage, NotFoundPage } from '../pages';
import { AuthProvider } from '../auth';
import { MemoryRouter } from 'react-router-dom';
function withRouter(node: React.ReactNode) { return render(<MemoryRouter><AuthProvider>{node}</AuthProvider></MemoryRouter>); }
describe('páginas principales', () => {
  it('muestra el formulario de acceso', () => { withRouter(<LoginPage />); expect(screen.getByRole('button', { name: /iniciar sesión/i })).toBeInTheDocument(); });
  it('muestra el estado vacío de clientes', async () => { vi.stubGlobal('fetch', vi.fn(() => Promise.resolve({ ok: true, json: () => Promise.resolve([]) }))); withRouter(<ClientsPage />); expect(await screen.findByText(/no hay clientes/i)).toBeInTheDocument(); });
  it('muestra la página no encontrada', () => { withRouter(<NotFoundPage />); expect(screen.getByText('404')).toBeInTheDocument(); });
});
