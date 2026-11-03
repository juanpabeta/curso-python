import { Link, NavLink } from 'react-router-dom';
import type { ReactNode } from 'react';
import { useAuth } from './auth';
export function Layout({ children }: { children: ReactNode }) { const { logout } = useAuth(); return <div className="app"><aside><Link className="brand" to="/">✈ <span>itinera</span></Link><nav><NavLink to="/">Resumen</NavLink><NavLink to="/clientes">Clientes</NavLink><NavLink to="/oportunidades">Oportunidades</NavLink><NavLink to="/recordatorios">Recordatorios</NavLink><NavLink to="/informes">Informes</NavLink></nav><button className="logout" onClick={() => void logout()}>Cerrar sesión</button></aside><main><header><span>CRM de agencia de viajes</span><strong>Hoy, {new Date().toLocaleDateString('es-ES', { day: 'numeric', month: 'long' })}</strong></header>{children}</main></div> }
export function Card({ title, value, hint }: { title: string; value: ReactNode; hint?: string }) { return <article className="metric"><span>{title}</span><b>{value}</b>{hint && <small>{hint}</small>}</article> }
export function Loading() { return <p className="loading">Cargando…</p> }
export function ErrorMessage({ message }: { message: string }) { return <div className="error">{message}</div> }
