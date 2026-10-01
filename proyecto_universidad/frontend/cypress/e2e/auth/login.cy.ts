import { assertJsonBody, assertLoginContract, assertResponseTime, assertStatus } from '../../helpers/assertions';
import { buildExpiredJwt } from '../../helpers/jwt';
import { apiUrl, authTokenKey, authUserKey } from '../../helpers/env';
import { loginPage } from '../../pages/login.page';

const assertSignedOut = (): void => {
  cy.window().then((win) => {
    expect(win.sessionStorage.getItem(authTokenKey())).to.equal(null);
    expect(win.sessionStorage.getItem(authUserKey())).to.equal(null);
  });
};

describe('Autenticación', () => {
  beforeEach(() => {
    cy.clearClientState();
  });

  it('inicia sesión con credenciales válidas y persiste un JWT usable', () => {
    cy.getFixtureUser('student').then((student) => {
      cy.spyAuthApi();

      loginPage.login(student.email, student.password);

      cy.wait('@authLogin').then((interception) => {
        assertStatus(interception, 200);
        assertJsonBody(interception);
        assertLoginContract(interception.response?.body as { access_token: string; token_type: string });
        assertResponseTime(interception);
        expect(interception.request.body).to.deep.include({
          email: student.email,
          password: student.password,
        });
        Cypress.env('accessToken', (interception.response?.body as { access_token: string }).access_token);
      });

      cy.wait('@authMe').then((interception) => {
        assertStatus(interception, 200);
        assertJsonBody(interception);
        assertResponseTime(interception);
        expect(interception.response?.body).to.include({
          email: student.email,
          full_name: student.fullName,
        });
        expect(interception.response?.body.roles).to.include(student.role);
      });

      cy.location('pathname').should('eq', student.dashboardPath);
      cy.findByRole('heading', { name: student.dashboardHeading }).should('be.visible');
      cy.get('.user-card').should('contain.text', student.fullName);
      cy.window().then((win) => {
        expect(win.sessionStorage.getItem(authTokenKey())).to.be.a('string').and.not.be.empty;
      });
    });
  });

  it('rechaza credenciales inválidas en UI y API', () => {
    cy.getFixtureUser('invalid').then((invalid) => {
      cy.spyAuthApi();
      loginPage.login(invalid.email, invalid.password);

      cy.wait('@authLogin').then((interception) => {
        assertJsonBody(interception);
        expect(interception.response?.statusCode).to.be.oneOf([401, 422]);
        expect(interception.response?.body).to.have.property('detail');
        expect(interception.response?.body).to.not.have.property('access_token');
        assertResponseTime(interception);
      });

      loginPage.alert().should('be.visible');
      cy.location('pathname').should('eq', '/login');
      assertSignedOut();
    });
  });

  it('bloquea el envío cuando las credenciales están vacías', () => {
    cy.spyAuthApi();
    loginPage.visit();
    loginPage.email().clear();
    loginPage.password().clear();
    loginPage.submitForm();

    loginPage.alert().should('contain.text', 'correo válido');
    cy.get('@authLogin.all').should('have.length', 0);
    cy.location('pathname').should('eq', '/login');
    assertSignedOut();
  });

  it('expone el token expirado como 401 y redirige al login', () => {
    const expired = buildExpiredJwt();

    cy.request({
      method: 'GET',
      url: `${apiUrl()}/auth/me`,
      headers: { Authorization: `Bearer ${expired}` },
      failOnStatusCode: false,
    }).then((response) => {
      expect(response.status).to.eq(401);
      expect(response.headers['content-type']).to.match(/json/i);
      expect(response.body).to.have.property('detail');
    });

    cy.intercept('GET', /\/auth\/me$/, {
      statusCode: 401,
      body: { detail: 'Token inválido o expirado' },
      headers: { 'content-type': 'application/json' },
    }).as('expiredSession');

    cy.visit('/student', {
      onBeforeLoad(win) {
        win.sessionStorage.setItem(authTokenKey(), expired);
        win.sessionStorage.setItem(
          authUserKey(),
          JSON.stringify({
            id: 2,
            email: 'student@universidad.test',
            full_name: 'Estudiante E2E',
            roles: ['Estudiante'],
          }),
        );
      },
    });

    cy.wait('@expiredSession').then((interception) => {
      assertStatus(interception, 401);
      assertJsonBody(interception);
      expect(interception.response?.body).to.deep.include({ detail: 'Token inválido o expirado' });
    });
    cy.location('pathname').should('eq', '/login');
    loginPage.title().should('be.visible');
    assertSignedOut();
  });

  it('muestra un error accesible si se pierde la conexión durante el login', () => {
    cy.getFixtureUser('student').then((student) => {
      cy.stubLoginNetworkError();
      loginPage.login(student.email, student.password);
      cy.wait('@authLoginDown').then((interception) => {
        expect(interception.response, 'un corte de red no tiene respuesta HTTP').to.equal(undefined);
      });
      loginPage.alert().should('be.visible');
      cy.location('pathname').should('eq', '/login');
      assertSignedOut();
    });
  });

  it('muestra el detalle cuando el login responde 503', () => {
    cy.getFixtureUser('student').then((student) => {
      cy.stubLoginServerDown();
      loginPage.login(student.email, student.password);

      cy.wait('@authLoginDown').then((interception) => {
        assertStatus(interception, 503);
        assertJsonBody(interception);
        expect(interception.response?.body).to.have.property('detail');
      });

      loginPage.alert().should('contain.text', 'Error interno del servidor');
      cy.location('pathname').should('eq', '/login');
      assertSignedOut();
    });
  });
});
