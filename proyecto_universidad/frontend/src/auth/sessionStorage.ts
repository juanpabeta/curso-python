import type { UserSession } from '@/types';

export const AUTH_TOKEN_STORAGE_KEY = 'universidad.session.token';
export const AUTH_USER_STORAGE_KEY = 'universidad.session.user';

export const readStoredToken = (): string | null => {
  try {
    return sessionStorage.getItem(AUTH_TOKEN_STORAGE_KEY);
  } catch {
    return null;
  }
};

export const readStoredUser = (): UserSession | null => {
  try {
    const raw = sessionStorage.getItem(AUTH_USER_STORAGE_KEY);
    return raw ? (JSON.parse(raw) as UserSession) : null;
  } catch {
    return null;
  }
};

export const persistSession = (token: string, user: UserSession | null): void => {
  sessionStorage.setItem(AUTH_TOKEN_STORAGE_KEY, token);
  if (user) {
    sessionStorage.setItem(AUTH_USER_STORAGE_KEY, JSON.stringify(user));
  }
};

export const clearPersistedSession = (): void => {
  sessionStorage.removeItem(AUTH_TOKEN_STORAGE_KEY);
  sessionStorage.removeItem(AUTH_USER_STORAGE_KEY);
};
