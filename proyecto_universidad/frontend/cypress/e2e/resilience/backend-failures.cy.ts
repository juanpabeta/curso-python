import { apiUrl, timeoutBackendMs } from '../../helpers/env';
import { buildTaskTitle } from '../../helpers/factories';
import { assertJsonBody, assertStatus } from '../../helpers/assertions';
import { taskBoardPage } from '../../pages/taskBoard.page';

describe('Resiliencia frente a fallos reales del backend', () => {
  beforeEach(() => {
    cy.ensureSession('student');
  });

  it('no renderiza basura cuando la lista llega corrupta', () => {
    cy.stubTasksCorrupt();
    cy.visit('/student');
    cy.wait('@listTasksCorrupt').then((interception) => {
      assertStatus(interception, 200);
      assertJsonBody(interception);
      expect(interception.response?.body).to.not.be.an('array');
    });
    cy.findByRole('alert').should('contain.text', 'No se pudieron cargar las tareas.');
    cy.findByRole('list', { name: /lista de tareas/i }).should('not.exist');
  });

  it('muestra carga y error cuando el listado termina en timeout HTTP', () => {
    const delay = timeoutBackendMs();
    cy.stubTasksTimeout();
    cy.then(() => {
      Cypress.env('timeoutStartedAt', Date.now());
    });
    cy.visit('/student');
    cy.contains('[role="status"]', 'Cargando tareas...').should('be.visible');
    cy.wait('@listTasksTimeout').then((interception) => {
      const elapsed = Date.now() - Number(Cypress.env('timeoutStartedAt'));
      assertStatus(interception, 504);
      assertJsonBody(interception);
      expect(interception.response?.body).to.deep.include({ detail: 'Gateway Timeout' });
      expect(elapsed, `timeout simulado (${elapsed}ms)`).to.be.greaterThan(delay - 400);
    });
    cy.findByRole('alert').should('contain.text', 'No se pudieron cargar las tareas.');
    cy.findByRole('list', { name: /lista de tareas/i }).should('not.exist');
  });

  it('detecta validaciones inconsistentes entre UI y backend', () => {
    cy.loginByApi('student').then((token) => {
      cy.request({
        method: 'POST',
        url: `${apiUrl()}/tasks/`,
        headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
        body: { title: '   ' },
        failOnStatusCode: false,
      }).then((response) => {
        expect(response.status).to.eq(422);
        expect(response.headers['content-type']).to.match(/json/i);
        expect(response.body).to.have.property('detail');
        expect(response.duration).to.be.lessThan(Number(Cypress.env('maxResponseMs') ?? 3000));
      });
    });

    cy.intercept('POST', /\/tasks\/?$/, {
      statusCode: 422,
      body: { detail: 'El título contiene caracteres no permitidos' },
      headers: { 'content-type': 'application/json' },
    }).as('inconsistentValidation');

    cy.visit('/student');
    const title = buildTaskTitle('inconsistente');
    taskBoardPage.create(title);
    cy.wait('@inconsistentValidation').then((interception) => {
      assertStatus(interception, 422);
      assertJsonBody(interception);
      expect(interception.response?.body).to.have.property('detail');
    });
    taskBoardPage.alert().should('contain.text', 'No se pudo crear la tarea');
    cy.findByRole('checkbox', { name: title }).should('not.exist');
    cy.listTasksByApi().then((tasks) => {
      expect(tasks.some((task) => task.title === title)).to.eq(false);
    });
  });

  it('rechaza una respuesta parcial que no cumple el contrato de tarea', () => {
    cy.stubTasksPartialCreate();
    cy.visit('/student');

    const title = buildTaskTitle('parcial');
    taskBoardPage.create(title);
    cy.wait('@createTaskPartial').then((interception) => {
      assertStatus(interception, 201);
      assertJsonBody(interception);
      expect(interception.response?.body).to.not.have.property('title');
      expect(interception.response?.body).to.not.have.property('completed');
    });
    taskBoardPage.alert().should('contain.text', 'No se pudo crear la tarea');
    cy.findByRole('checkbox', { name: title }).should('not.exist');
    cy.listTasksByApi().then((tasks) => {
      expect(tasks.some((task) => task.title === title)).to.eq(false);
    });
  });
});
