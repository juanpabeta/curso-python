export const apiUrl = (): string => String(Cypress.env('apiUrl') ?? 'http://127.0.0.1:8000');

export const maxResponseMs = (): number => Number(Cypress.env('maxResponseMs') ?? 3000);

export const slowBackendMs = (): number => Number(Cypress.env('slowBackendMs') ?? 1800);

export const timeoutBackendMs = (): number => Number(Cypress.env('timeoutBackendMs') ?? 2500);

export const authTokenKey = (): string =>
  String(Cypress.env('authTokenKey') ?? 'universidad.session.token');

export const authUserKey = (): string =>
  String(Cypress.env('authUserKey') ?? 'universidad.session.user');
