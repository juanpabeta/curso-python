import { apiRequest } from '../../helpers/apiClient';
import { assertLoginContract } from '../../helpers/assertions';
import { authTokenKey } from '../../helpers/env';
import { loginPage } from '../../pages/login.page';
import { dashboardPage } from '../../pages/dashboard.page';
import { registerAuthSpies } from '../intercepts';

const defaultUserKey: AcademicUserKey = 'student';

const resolveAccount = (user: AcademicUserKey | AcademicUser = defaultUserKey) =>
  typeof user === 'string' ? cy.getFixtureUser(user) : cy.wrap(user);

Cypress.Commands.add('getFixtureUser', (key: AcademicUserKey = defaultUserKey) => {
  return cy.fixture<Record<AcademicUserKey, AcademicUser>>('users.json').then((users) => {
    const overrides = (Cypress.env('users') ?? {}) as Partial<Record<AcademicUserKey, Partial<AcademicUser>>>;
    return { ...users[key], ...overrides[key] };
  });
});

Cypress.Commands.add('clearClientState', () => {
  Cypress.session.clearAllSavedSessions();
  Cypress.env('accessToken', null);

  return cy
    .visit('/login', {
      onBeforeLoad(win) {
        win.sessionStorage.clear();
        win.localStorage.clear();
      },
    })
    .then(() => {
      cy.clearCookies();
    });
});

Cypress.Commands.add('loginByUi', (user: AcademicUserKey | AcademicUser = defaultUserKey) => {
  return resolveAccount(user).then((account) => {
    registerAuthSpies();
    loginPage.login(account.email, account.password);

    cy.wait('@authLogin').then(({ response }) => {
      expect(response?.statusCode).to.eq(200);
      assertLoginContract(response?.body as { access_token: string; token_type: string });
      Cypress.env('accessToken', (response?.body as { access_token: string }).access_token);
    });

    cy.wait('@authMe').its('response.statusCode').should('eq', 200);
    cy.location('pathname').should('eq', account.dashboardPath ?? '/student');
    dashboardPage.assertAuthenticated(account.dashboardHeading ?? /panel/i, account.fullName);
  });
});

Cypress.Commands.add('loginByApi', (user: AcademicUserKey | AcademicUser = defaultUserKey) => {
  return resolveAccount(user).then((account) =>
    apiRequest('POST', '/auth/login', {
      body: { email: account.email, password: account.password },
    }).then((response) => {
      expect(response.status).to.eq(200);
      assertLoginContract(response.body as { access_token: string; token_type: string });
      const token = (response.body as { access_token: string }).access_token;
      Cypress.env('accessToken', token);
      return token;
    }),
  );
});

Cypress.Commands.add('ensureSession', (user: AcademicUserKey = defaultUserKey) => {
  return cy.getFixtureUser(user).then((account) => {
    return cy.session(
      account.email,
      () => cy.loginByUi(account),
      {
        cacheAcrossSpecs: false,
        validate() {
          cy.window().then((win) => {
            const token = win.sessionStorage.getItem(authTokenKey());
            expect(token, 'token de sesión').to.be.a('string').and.not.be.empty;
            Cypress.env('accessToken', token);
          });
        },
      },
    );
  });
});

Cypress.Commands.add('logoutByUi', () => {
  registerAuthSpies();
  dashboardPage.logout().click();
  cy.wait('@authLogout').its('response.statusCode').should('eq', 200);
  cy.location('pathname').should('eq', '/login');
});
