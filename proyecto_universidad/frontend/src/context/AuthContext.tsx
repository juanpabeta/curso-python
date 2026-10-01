import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type PropsWithChildren,
} from 'react';
import { api, setRuntimeToken, subscribeUnauthorized } from '@/api/client';
import {
  clearPersistedSession,
  persistSession,
  readStoredToken,
  readStoredUser,
} from '@/auth/sessionStorage';
import type { RoleName, UserSession } from '@/types';
import { toUserMessage } from '@/utils/errors';

interface AuthContextValue {
  user: UserSession | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  sessionNotice: string;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  clearSessionNotice: () => void;
  hasRole: (role: string) => boolean;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

const decodeJwtPayload = (token: string): UserSession | null => {
  try {
    const base64 = token.split('.')[1];
    if (!base64) {
      return null;
    }
    const payload = JSON.parse(atob(base64.replace(/-/g, '+').replace(/_/g, '/')));
    const roles = (Array.isArray(payload.roles) ? payload.roles : []).filter(
      (role: unknown): role is RoleName =>
        ['Administrador', 'Docente', 'Estudiante'].includes(String(role) as RoleName),
    );

    return {
      id: Number(payload.sub ?? 0),
      email: String(payload.email ?? ''),
      full_name: String(payload.full_name ?? 'Usuario'),
      roles,
    };
  } catch {
    return null;
  }
};

export const AuthProvider = ({ children }: PropsWithChildren) => {
  const [user, setUser] = useState<UserSession | null>(() => readStoredUser());
  const [token, setToken] = useState<string | null>(() => readStoredToken());
  const [isLoading, setIsLoading] = useState(false);
  const [isRestoring, setIsRestoring] = useState(() => Boolean(readStoredToken()));
  const [sessionNotice, setSessionNotice] = useState('');

  const clearSession = useCallback(() => {
    setRuntimeToken(null);
    setToken(null);
    setUser(null);
    clearPersistedSession();
  }, []);

  const applySession = useCallback((nextToken: string, nextUser: UserSession | null) => {
    setRuntimeToken(nextToken);
    setToken(nextToken);
    setUser(nextUser);
    persistSession(nextToken, nextUser);
  }, []);

  useEffect(() => {
    const storedToken = readStoredToken();
    if (!storedToken) {
      setIsRestoring(false);
      return;
    }

    setRuntimeToken(storedToken);
    let cancelled = false;

    api
      .get<UserSession>('/auth/me')
      .then((response) => {
        if (!cancelled) {
          applySession(storedToken, response.data);
        }
      })
      .catch(() => {
        if (!cancelled) {
          clearSession();
        }
      })
      .finally(() => {
        if (!cancelled) {
          setIsRestoring(false);
        }
      });

    return () => {
      cancelled = true;
    };
  }, [applySession, clearSession]);

  useEffect(
    () =>
      subscribeUnauthorized(() => {
        const hadSession = Boolean(readStoredToken());
        clearSession();
        if (hadSession) {
          setSessionNotice('Tu sesión expiró. Vuelve a iniciar sesión.');
        }
      }),
    [clearSession],
  );

  const hasRole = useCallback(
    (role: string) =>
      user?.roles.some((userRole) => userRole.toLowerCase() === role.toLowerCase()) ?? false,
    [user],
  );

  const login = useCallback(
    async (email: string, password: string) => {
      setIsLoading(true);
      setSessionNotice('');
      try {
        const response = await api.post<{ access_token: string; token_type: string }>('/auth/login', {
          email,
          password,
        });

        const nextToken = response.data.access_token;
        setRuntimeToken(nextToken);

        try {
          const me = await api.get<UserSession>('/auth/me');
          applySession(nextToken, me.data);
        } catch {
          applySession(nextToken, decodeJwtPayload(nextToken));
        }
      } catch (error) {
        throw new Error(toUserMessage(error, 'Error al iniciar sesión.'));
      } finally {
        setIsLoading(false);
      }
    },
    [applySession],
  );

  const logout = useCallback(async () => {
    try {
      await api.post('/auth/logout');
    } finally {
      clearSession();
    }
  }, [clearSession]);

  const clearSessionNotice = useCallback(() => setSessionNotice(''), []);

  const value = useMemo<AuthContextValue>(
    () => ({
      user,
      token,
      isAuthenticated: Boolean(user && token),
      isLoading: isLoading || isRestoring,
      sessionNotice,
      login,
      logout,
      clearSessionNotice,
      hasRole,
    }),
    [user, token, isLoading, isRestoring, sessionNotice, login, logout, clearSessionNotice, hasRole],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = (): AuthContextValue => {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error('useAuth must be used inside an AuthProvider');
  }

  return context;
};
