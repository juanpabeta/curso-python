import { apiUrl } from './env';

interface RequestOptions {
  token?: string;
  failOnStatusCode?: boolean;
  body?: unknown;
}

const withAuth = (token?: string): Record<string, string> =>
  token ? { Authorization: `Bearer ${token}` } : {};

export const apiRequest = (
  method: string,
  path: string,
  options: RequestOptions = {},
): Cypress.Chainable<Cypress.Response<unknown>> =>
  cy.request({
    method,
    url: `${apiUrl()}${path}`,
    body: options.body,
    headers: {
      'Content-Type': 'application/json',
      ...withAuth(options.token),
    },
    failOnStatusCode: options.failOnStatusCode ?? true,
  });
