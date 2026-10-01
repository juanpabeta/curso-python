import { assertJsonBody, assertStatus, assertTaskContract } from '../../helpers/assertions';
import { buildTaskTitle } from '../../helpers/factories';
import { taskBoardPage } from '../../pages/taskBoard.page';
import { dashboardPage } from '../../pages/dashboard.page';

describe('Visualización de tareas', () => {
  beforeEach(() => {
    cy.ensureSession('student');
    cy.deleteTasksByTitlePrefix('e2e-tarea-');
  });

  afterEach(() => {
    cy.deleteTasksByTitlePrefix('e2e-tarea-');
  });

  it('pinta en la lista los mismos datos que persistió la API', () => {
    const title = buildTaskTitle('lista');

    cy.spyTasksApi();
    cy.visit('/student');
    cy.wait('@listTasks').then((interception) => {
      assertStatus(interception, 200);
      assertJsonBody(interception);
    });
    taskBoardPage.create(title);

    cy.wait('@createTask').then((interception) => {
      assertStatus(interception, 201);
      assertTaskContract(interception.response?.body as AcademicTask);
      expect(interception.response?.body).to.include({ title, completed: false });
    });

    taskBoardPage.list().should('contain.text', title);
    taskBoardPage.item(title).should('be.visible').and('not.be.checked');

    cy.listTasksByApi().then((tasks) => {
      const persisted = tasks.find((task) => task.title === title);
      expect(persisted, 'la API debe devolver la tarea recién creada').to.exist;
      expect(persisted?.completed).to.eq(false);
      cy.findByRole('checkbox', { name: persisted?.title ?? title }).should('exist');
    });
  });

  it('mantiene la tarea después de recargar el dashboard', () => {
    const title = buildTaskTitle('refresco');
    cy.spyTasksApi();
    cy.visit('/student');
    cy.wait('@listTasks');
    taskBoardPage.create(title);
    cy.wait('@createTask');
    taskBoardPage.assertVisible(title);

    cy.intercept('GET', /\/auth\/me$/, (req) => {
      const started = Date.now();
      req.continue((res) => {
        res.headers['x-e2e-elapsed-ms'] = String(Date.now() - started);
      });
    }).as('sessionRestored');
    cy.intercept('GET', /\/tasks\/?$/, (req) => {
      const started = Date.now();
      req.continue((res) => {
        res.headers['x-e2e-elapsed-ms'] = String(Date.now() - started);
      });
    }).as('tasksAfterReload');

    cy.reload();
    cy.wait('@sessionRestored').then((interception) => {
      assertStatus(interception, 200);
      assertJsonBody(interception);
      expect(interception.response?.body.roles).to.include('Estudiante');
    });
    cy.wait('@tasksAfterReload').then((interception) => {
      assertStatus(interception, 200);
      assertJsonBody(interception);
      const tasks = interception.response?.body as AcademicTask[];
      expect(tasks.some((task) => task.title === title && task.completed === false)).to.eq(true);
    });

    cy.getFixtureUser('student').then((student) => {
      dashboardPage.assertAuthenticated(student.dashboardHeading, student.fullName);
    });
    taskBoardPage.item(title).should('be.visible').and('not.be.checked');
  });
});
