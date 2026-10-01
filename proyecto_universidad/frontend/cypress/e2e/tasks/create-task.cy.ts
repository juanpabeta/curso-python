import { assertJsonBody, assertResponseTime, assertStatus, assertTaskContract } from '../../helpers/assertions';
import { buildTaskTitle } from '../../helpers/factories';
import { slowBackendMs } from '../../helpers/env';
import { taskBoardPage } from '../../pages/taskBoard.page';

describe('Creación de tarea académica', () => {
  beforeEach(() => {
    cy.ensureSession('student');
    cy.deleteTasksByTitlePrefix('e2e-tarea-');
  });

  afterEach(() => {
    cy.deleteTasksByTitlePrefix('e2e-tarea-');
  });

  it('crea una tarea válida y mantiene consistencia UI + API', () => {
    const title = buildTaskTitle('valida');
    cy.spyTasksApi();
    cy.visit('/student');
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
      expect(interception.request.body).to.deep.equal({ title });
      expect(interception.response?.body).to.include({ title, completed: false });
    });

    taskBoardPage.assertVisible(title);
    cy.listTasksByApi().then((tasks) => {
      const persisted = tasks.find((task) => task.title === title);
      expect(persisted, 'la tarea debe persistir').to.exist;
      expect(persisted?.completed).to.eq(false);
    });
  });

  it('no llama al backend cuando el título es inválido', () => {
    cy.spyTasksApi();
    cy.visit('/student');
    cy.wait('@listTasks');

    cy.fixture<{ blankTitle: string; tooLongTitle: string }>('tasks.json').then((samples) => {
      expect(samples.blankTitle.trim(), 'fixture de título vacío').to.eq('');
      expect(samples.tooLongTitle.length, 'fixture de título largo').to.be.greaterThan(120);

      taskBoardPage.titleInput().clear().type(samples.blankTitle);
      taskBoardPage.submit().click();
      taskBoardPage.alert().should('contain.text', 'Escribe el título de la tarea.');
      cy.get('@createTask.all').should('have.length', 0);

      taskBoardPage.titleInput().clear().type(samples.tooLongTitle, { delay: 0 });
      taskBoardPage.submit().click();
      taskBoardPage.alert().should('contain.text', '120 caracteres');
      cy.get('@createTask.all').should('have.length', 0);
    });

    cy.listTasksByApi().then((tasks) => {
      expect(tasks.some((task) => task.title.trim() === '' || task.title.length > 120)).to.eq(false);
    });
  });

  it('muestra error de UI cuando el backend responde 500 y no persiste la tarea', () => {
    const title = buildTaskTitle('500');
    cy.stubCreateTaskError(500);
    cy.visit('/student');

    taskBoardPage.create(title);
    cy.wait('@createTaskError').then((interception) => {
      assertStatus(interception, 500);
      assertJsonBody(interception);
      expect(interception.response?.body).to.have.property('detail');
    });
    taskBoardPage.alert().should('contain.text', 'No se pudo crear la tarea');
    cy.findByRole('checkbox', { name: title }).should('not.exist');
    cy.listTasksByApi().then((tasks) => {
      expect(tasks.some((task) => task.title === title)).to.eq(false);
    });
  });

  it('deshabilita el envío mientras el backend es lento', () => {
    const title = buildTaskTitle('lenta');
    const delay = slowBackendMs();
    cy.stubCreateTaskDelay(delay, {
      id: crypto.randomUUID(),
      title,
      completed: false,
    });
    cy.visit('/student');

    taskBoardPage.titleInput().type(title);
    cy.then(() => {
      Cypress.env('slowStartedAt', Date.now());
    });
    taskBoardPage.submit().click();
    cy.findByRole('button', { name: /agregando/i }).should('be.disabled');
    cy.wait('@createTaskSlow').then((interception) => {
      const elapsed = Date.now() - Number(Cypress.env('slowStartedAt'));
      assertStatus(interception, 201);
      assertJsonBody(interception);
      assertTaskContract(interception.response?.body as AcademicTask);
      expect(interception.response?.body).to.include({ title, completed: false });
      expect(elapsed, `latencia simulada (${elapsed}ms)`).to.be.greaterThan(delay - 400);
    });
    cy.findByRole('button', { name: /agregar tarea/i }).should('be.enabled');
    taskBoardPage.assertVisible(title);
  });

  it('informa la pérdida de conexión al crear y no deja datos persistidos', () => {
    cy.stubCreateTaskOffline();
    cy.visit('/student');

    const title = buildTaskTitle('offline');
    taskBoardPage.create(title);
    cy.wait('@createTaskOffline').then((interception) => {
      expect(interception.response, 'la petición offline no tiene respuesta').to.equal(undefined);
    });
    taskBoardPage.alert().should('contain.text', 'No se pudo crear la tarea');
    cy.findByRole('checkbox', { name: title }).should('not.exist');
    cy.listTasksByApi().then((tasks) => {
      expect(tasks.some((task) => task.title === title)).to.eq(false);
    });
  });
});
