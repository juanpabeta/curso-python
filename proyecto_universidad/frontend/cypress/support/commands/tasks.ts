import { apiRequest } from '../../helpers/apiClient';
import { assertTaskContract } from '../../helpers/assertions';
import {
  stubCreateTaskDelay,
  stubCreateTaskError,
  stubCreateTaskOffline,
  stubLoginNetworkError,
  stubLoginServerDown,
  stubTasksCorrupt,
  stubTasksPartialCreate,
  stubTasksTimeout,
} from '../intercepts';

const tokenOrStored = (token?: string): Cypress.Chainable<string> => {
  if (token) {
    return cy.wrap(token, { log: false });
  }

  const stored = Cypress.env('accessToken') as string | undefined;
  if (stored) {
    return cy.wrap(stored, { log: false });
  }

  return cy.loginByApi('student');
};

Cypress.Commands.add('createTaskByApi', (title: string, token?: string) => {
  return tokenOrStored(token).then((accessToken) =>
    apiRequest('POST', '/tasks/', {
      token: accessToken,
      body: { title },
    }).then((response) => {
      expect(response.status).to.eq(201);
      const task = response.body as AcademicTask;
      assertTaskContract(task);
      expect(task.title).to.eq(title);
      return task;
    }),
  );
});

Cypress.Commands.add('listTasksByApi', (token?: string) => {
  return tokenOrStored(token).then((accessToken) =>
    apiRequest('GET', '/tasks/', { token: accessToken }).then((response) => {
      expect(response.status).to.eq(200);
      expect(response.body).to.be.an('array');
      return response.body as AcademicTask[];
    }),
  );
});

Cypress.Commands.add('deleteTaskByApi', (id: string, token?: string) => {
  return tokenOrStored(token).then((accessToken) => {
    return apiRequest('DELETE', `/tasks/${id}`, { token: accessToken }).then((response) => {
      expect(response.status).to.eq(204);
    });
  });
});

Cypress.Commands.add('deleteTasksByTitlePrefix', (prefix: string, token?: string) => {
  return tokenOrStored(token).then((accessToken) => {
    return cy.listTasksByApi(accessToken).then((tasks) => {
      const owned = tasks.filter((task) => task.title.startsWith(prefix));
      return cy.wrap(owned, { log: false }).each((task) => {
        cy.deleteTaskByApi(task.id, accessToken);
      });
    });
  });
});

Cypress.Commands.add('stubLoginNetworkError', stubLoginNetworkError);
Cypress.Commands.add('stubLoginServerDown', stubLoginServerDown);
Cypress.Commands.add('stubCreateTaskError', stubCreateTaskError);
Cypress.Commands.add('stubCreateTaskDelay', stubCreateTaskDelay);
Cypress.Commands.add('stubCreateTaskOffline', stubCreateTaskOffline);
Cypress.Commands.add('stubTasksCorrupt', stubTasksCorrupt);
Cypress.Commands.add('stubTasksPartialCreate', stubTasksPartialCreate);
Cypress.Commands.add('stubTasksTimeout', stubTasksTimeout);
