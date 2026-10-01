export interface CypressProfile {
  baseUrl: string;
  apiUrl: string;
  maxResponseMs: number;
}

export const profiles: Record<string, CypressProfile> = {
  local: {
    baseUrl: 'http://localhost:3000',
    apiUrl: 'http://127.0.0.1:8000',
    maxResponseMs: 3000,
  },
  ci: {
    baseUrl: 'http://localhost:3000',
    apiUrl: 'http://127.0.0.1:8000',
    maxResponseMs: 8000,
  },
};

export const profileNames = Object.keys(profiles);
