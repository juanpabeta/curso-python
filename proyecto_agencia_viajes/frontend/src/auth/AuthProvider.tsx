import { createContext, useContext, useEffect, useMemo, useState, type ReactNode } from 'react';
import { api } from '../api';
import { onUnauthorized } from '../api/client';
import type { User } from '../types';
type Auth = { user: User | null; loading: boolean; login: (u: string, p: string) => Promise<void>; logout: () => Promise<void> };
const Context = createContext<Auth | null>(null);
export function AuthProvider({ children }: { children: ReactNode }) { const [user, setUser] = useState<User | null>(null); const [loading, setLoading] = useState(true); useEffect(() => { const cleanup = onUnauthorized(() => setUser(null)); api.me().then(setUser).catch(() => setUser(null)).finally(() => setLoading(false)); return cleanup; }, []); const value = useMemo<Auth>(() => ({ user, loading, async login(u, p) { setUser(await api.login(u, p)); }, async logout() { try { await api.logout(); } finally { setUser(null); } } }), [user, loading]); return <Context.Provider value={value}>{children}</Context.Provider>; }
export function useAuth() { const value = useContext(Context); if (!value) throw new Error('useAuth debe usarse dentro de AuthProvider'); return value; }
