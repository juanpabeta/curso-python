import { apiUrl } from '../../helpers/env';
import { buildTaskTitle } from '../../helpers/factories';
import { assertJsonBody, assertResponseTime, assertStatus, assertTaskContract } from '../../helpers/assertions';
import { taskBoardPage } from '../../pages/taskBoard.page';

describe('Confirmación de creación', () => {
  beforeEach(() => {
    cy.ensureSession('student');
    cy.deleteTasksByTitlePrefix('e2e-tarea-');
    cy.spyTasksApi();
    cy.visit('/student');
    cy.wait('@listTasks');
  });

  afterEach(() => {
    cy.deleteTasksByTitlePrefix('e2e-tarea-');
  });

  it('confirma visualmente, por API y en persistencia', () => {
    const title = buildTaskTitle('confirmacion');
    taskBoardPage.create(title);

    cy.wait('@createTask').then((interception) => {
      assertStatus(interception, 201);
      assertJsonBody(interception);
      assertResponseTime(interception);
      const created = interception.response?.body as AcademicTask;
      assertTaskContract(created);
      expect(created).to.include({ title, completed: false });
      taskBoardPage.assertVisible(created.title);

      cy.loginByApi('student').then((token) => {
        cy.request({
          method: 'GET',
          url: `${apiUrl()}/tasks/${created.id}`,
          headers: { Authorization: `Bearer ${token}` },
        }).then((response) => {
          expect(response.status).to.eq(200);
          expect(response.headers['content-type']).to.match(/json/i);
          expect(response.duration, 'tiempo del GET por id').to.be.lessThan(Number(Cypress.env('maxResponseMs') ?? 3000));
          expect(response.body).to.deep.include({
            id: created.id,
            title: created.title,
            completed: false,
          });
        });

        cy.listTasksByApi(token).then((tasks) => {
          const persisted = tasks.find((task) => task.id === created.id);
          expect(persisted, 'la tarea debe persistir en el listado remoto').to.exist;
          expect(persisted).to.deep.include({
            id: created.id,
            title,
            completed: false,
          });
        });
      });
    });
  });
});
