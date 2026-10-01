import { buildTaskPayload } from '../helpers/factories';
import { slowBackendMs, timeoutBackendMs } from '../helpers/env';

const LOGIN = /\/auth\/login$/;
const LOGOUT = /\/auth\/logout$/;
const ME = /\/auth\/me$/;
const TASK_COLLECTION = /\/tasks\/?$/;
const TASK_BY_ID = /\/tasks\/[^/]+$/;

type StampableRequest = {
  continue: (callback: (res: { headers: Record<string, string> }) => void) => void;
};

export const stampElapsed = (req: StampableRequest): void => {
  const started = Date.now();
  req.continue((res) => {
    res.headers['x-e2e-elapsed-ms'] = String(Date.now() - started);
  });
};

export const registerAuthSpies = (): void => {
  cy.intercept('POST', LOGIN, stampElapsed).as('authLogin');
  cy.intercept('POST', LOGOUT, stampElapsed).as('authLogout');
  cy.intercept('GET', ME, stampElapsed).as('authMe');
};

export const registerTaskSpies = (): void => {
  cy.intercept('GET', TASK_COLLECTION, stampElapsed).as('listTasks');
  cy.intercept('POST', TASK_COLLECTION, stampElapsed).as('createTask');
  cy.intercept('GET', TASK_BY_ID, stampElapsed).as('getTask');
};

export const stubLoginNetworkError = (): void => {
  cy.intercept('POST', LOGIN, { forceNetworkError: true }).as('authLoginDown');
};

export const stubLoginServerDown = (): void => {
  cy.intercept('POST', LOGIN, {
    statusCode: 503,
    fixture: 'errors/server-error.json',
  }).as('authLoginDown');
};

export const stubCreateTaskError = (statusCode = 500): void => {
  cy.intercept('POST', TASK_COLLECTION, {
    statusCode,
    fixture: 'errors/server-error.json',
  }).as('createTaskError');
};

export const stubCreateTaskDelay = (delayMs = slowBackendMs(), body = buildTaskPayload()): void => {
  cy.intercept('POST', TASK_COLLECTION, (req) => {
    req.reply({
      delay: delayMs,
      statusCode: 201,
      body,
      headers: { 'content-type': 'application/json' },
    });
  }).as('createTaskSlow');
};

export const stubCreateTaskOffline = (): void => {
  cy.intercept('POST', TASK_COLLECTION, { forceNetworkError: true }).as('createTaskOffline');
};

export const stubTasksCorrupt = (): void => {
  cy.intercept('GET', TASK_COLLECTION, {
    statusCode: 200,
    fixture: 'errors/corrupt-tasks.json',
  }).as('listTasksCorrupt');
};

export const stubTasksPartialCreate = (): void => {
  cy.intercept('POST', TASK_COLLECTION, {
    statusCode: 201,
    fixture: 'errors/partial-task.json',
  }).as('createTaskPartial');
};

export const stubTasksTimeout = (): void => {
  cy.intercept('GET', TASK_COLLECTION, (req) => {
    req.reply({
      delay: timeoutBackendMs(),
      statusCode: 504,
      body: { detail: 'Gateway Timeout' },
      headers: { 'content-type': 'application/json' },
    });
  }).as('listTasksTimeout');
};
