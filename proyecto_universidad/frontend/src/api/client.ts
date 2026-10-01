import axios from 'axios';

let runtimeToken: string | null = null;
const unauthorizedListeners = new Set<() => void>();

export const setRuntimeToken = (token: string | null): void => {
  runtimeToken = token;
};

export const subscribeUnauthorized = (listener: () => void): (() => void) => {
  unauthorizedListeners.add(listener);
  return () => {
    unauthorizedListeners.delete(listener);
  };
};

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  if (runtimeToken) {
    config.headers = config.headers ?? {};
    config.headers.set?.('Authorization', `Bearer ${runtimeToken}`);
  }

  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    const status = error?.response?.status;
    const requestUrl = String(error?.config?.url ?? '');
    const isLoginAttempt = requestUrl.includes('/auth/login');

    if (status === 401) {
      setRuntimeToken(null);
      if (!isLoginAttempt) {
        unauthorizedListeners.forEach((listener) => listener());
      }
    }

    return Promise.reject(error);
  },
);
