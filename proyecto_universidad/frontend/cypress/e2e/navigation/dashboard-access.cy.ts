import { assertJsonBody, assertResponseTime, assertStatus } from '../../helpers/assertions';
import { loginPage } from '../../pages/login.page';
import { dashboardPage } from '../../pages/dashboard.page';

describe('Navegación y control de acceso', () => {
  it('bloquea el dashboard cuando no hay sesión y no consulta tareas', () => {
    cy.clearClientState();
    cy.spyTasksApi();
    cy.visit('/student');

    cy.location('pathname').should('eq', '/login');
    loginPage.title().should('be.visible');
    cy.get('@listTasks.all').should('have.length', 0);
  });

  it('permite el dashboard autenticado y serializa el perfil desde /auth/me', () => {
    cy.ensureSession('student');
    cy.spyAuthApi();
    cy.spyTasksApi();
    cy.visit('/student');

    cy.wait('@authMe').then((interception) => {
      assertStatus(interception, 200);
      assertJsonBody(interception);
      assertResponseTime(interception);
      expect(interception.response?.body).to.include.keys('email', 'full_name', 'roles');
      expect(interception.response?.body.roles).to.include('Estudiante');
    });

    cy.wait('@listTasks').then((interception) => {
      assertStatus(interception, 200);
      assertJsonBody(interception);
      assertResponseTime(interception);
      expect(interception.response?.body).to.be.an('array');
    });

    cy.getFixtureUser('student').then((student) => {
      dashboardPage.assertAuthenticated(student.dashboardHeading, student.fullName);
      cy.location('pathname').should('eq', '/student');
    });
  });

  it('niega a un estudiante el panel de administrador', () => {
    cy.ensureSession('student');
    cy.spyTasksApi();
    cy.visit('/admin');

    cy.location('pathname').should('eq', '/unauthorized');
    cy.findByRole('heading', { name: /acceso denegado/i }).should('be.visible');
    cy.get('@listTasks.all').should('have.length', 0);
  });
});
