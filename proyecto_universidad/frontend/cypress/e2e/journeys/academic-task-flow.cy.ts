import { assertJsonBody, assertLoginContract, assertResponseTime, assertStatus, assertTaskContract } from '../../helpers/assertions';
import { buildTaskTitle } from '../../helpers/factories';
import { loginPage } from '../../pages/login.page';
import { dashboardPage } from '../../pages/dashboard.page';
import { taskBoardPage } from '../../pages/taskBoard.page';

describe('Viaje académico completo', () => {
  beforeEach(() => {
    cy.deleteTasksByTitlePrefix('e2e-tarea-');
  });

  afterEach(() => {
    cy.deleteTasksByTitlePrefix('e2e-tarea-');
  });

  it('recorre login → dashboard → alta → confirmación → persistencia → visualización', () => {
    const title = buildTaskTitle('viaje');

    cy.clearClientState();
    cy.getFixtureUser('student').then((student) => {
      cy.spyAuthApi();
      cy.spyTasksApi();

      loginPage.login(student.email, student.password);

      cy.wait('@authLogin').then((interception) => {
        assertStatus(interception, 200);
        assertJsonBody(interception);
        assertLoginContract(interception.response?.body as { access_token: string; token_type: string });
        assertResponseTime(interception);
        Cypress.env('accessToken', (interception.response?.body as { access_token: string }).access_token);
      });

      cy.wait('@authMe').then((interception) => {
        assertStatus(interception, 200);
        assertJsonBody(interception);
        expect(interception.response?.body).to.include({
          email: student.email,
          full_name: student.fullName,
        });
        expect(interception.response?.body.roles).to.include('Estudiante');
      });

      cy.location('pathname').should('eq', '/student');
      dashboardPage.assertAuthenticated(student.dashboardHeading, student.fullName);
      cy.wait('@listTasks').then((interception) => {
        assertStatus(interception, 200);
        assertJsonBody(interception);
        expect(interception.response?.body).to.be.an('array');
      });

      taskBoardPage.create(title);

      cy.wait('@createTask').then((interception) => {
        assertStatus(interception, 201);
        assertJsonBody(interception);
        assertTaskContract(interception.response?.body as AcademicTask);
        assertResponseTime(interception);
        const created = interception.response?.body as AcademicTask;
        expect(created).to.include({ title, completed: false });
        taskBoardPage.assertVisible(created.title);

        cy.listTasksByApi().then((tasks) => {
          expect(tasks.map((task) => task.id)).to.include(created.id);
        });
      });

      cy.reload();
      dashboardPage.assertAuthenticated(student.dashboardHeading, student.fullName);
      taskBoardPage.item(title).should('be.visible').and('not.be.checked');
      cy.listTasksByApi().then((tasks) => {
        const persisted = tasks.find((task) => task.title === title);
        expect(persisted?.completed).to.eq(false);
      });
    });
  });
});
