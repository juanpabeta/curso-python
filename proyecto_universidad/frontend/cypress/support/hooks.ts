import { apiUrl } from '../helpers/env';

export const registerGlobalHooks = (): void => {
  before(() => {
    cy.request({
      url: `${Cypress.env('apiUrl')}/health`,
      failOnStatusCode: false,
    }).then((response) => {
      if (response.status !== 200) {
        throw new Error(
          `El backend no responde en ${Cypress.env('apiUrl')}. Arranca uvicorn antes de Cypress.`,
        );
      }
    });

    cy.ensureAcademicUsers();
  });

  beforeEach(() => {
    cy.intercept({ middleware: true, url: `${apiUrl()}/**` }, (req) => {
      req.on('response', (res) => {
        if (res.statusCode >= 500) {
          Cypress.log({
            name: 'http-5xx',
            message: `${req.method} ${req.url} → ${res.statusCode}`,
          });
        }
      });
    });
  });
};
