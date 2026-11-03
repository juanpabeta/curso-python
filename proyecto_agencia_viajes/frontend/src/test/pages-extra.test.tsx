import { render, screen } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { describe, expect, it, vi } from 'vitest';
import { AuthProvider } from '../auth';
import { ClientDetailPage } from '../pages/ClientDetailPage';
import { ReportsPage } from '../pages/ReportsPage';
vi.mock('../api', () => ({ api: { me: vi.fn(() => Promise.reject(new Error('anonymous'))), clients: vi.fn(() => Promise.resolve([{ id: 1, name: 'Ana', phone: '1', email: null, companions: [] }])), interactions: vi.fn(() => Promise.resolve([])), conversion: vi.fn(() => Promise.resolve({ won: 2, lost: 1 })), withoutContact: vi.fn(() => Promise.resolve([])) } }));
describe('detalle e informes', () => {
  it('muestra la ficha de cliente y sus formularios', async () => { render(<MemoryRouter initialEntries={['/clientes/1']}><AuthProvider><Routes><Route path="/clientes/:id" element={<ClientDetailPage />} /></Routes></AuthProvider></MemoryRouter>); expect(await screen.findByText('Ana')).toBeInTheDocument(); expect(screen.getByText('Acompañantes')).toBeInTheDocument(); });
  it('muestra métricas del informe', async () => { render(<MemoryRouter><AuthProvider><ReportsPage /></AuthProvider></MemoryRouter>); expect(await screen.findByText('Oportunidades ganadas')).toBeInTheDocument(); });
});
