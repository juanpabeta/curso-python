import { apiRequest } from '../../helpers/apiClient';
import { registerAuthSpies, registerTaskSpies } from '../intercepts';


const requiredUsers: AcademicUserKey[] = ['admin', 'teacher', 'student'];

Cypress.Commands.add('ensureAcademicUsers', () => {
  cy.wrap(requiredUsers, { log: false }).each((key: AcademicUserKey) =>
    cy.getFixtureUser(key).then((account) =>
      apiRequest('POST', '/auth/login', {
        body: { email: account.email, password: account.password },
        failOnStatusCode: false,
      }).then((login) => {
        if (login.status !== 200) {
          throw new Error(
            `No se pudo autenticar ${account.email} (HTTP ${login.status}). Desde backend ejecuta: python -m scripts.seed_e2e`,
          );
        }
      }),
    ),
  );
});

Cypress.Commands.add('spyAuthApi', registerAuthSpies);
Cypress.Commands.add('spyTasksApi', registerTaskSpies);
