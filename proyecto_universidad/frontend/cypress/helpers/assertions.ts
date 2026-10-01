import { maxResponseMs } from './env';

type TimedInterception = {
  response?: {
    statusCode?: number;
    body?: unknown;
    headers?: Record<string, string | string[]>;
  };
};

const headerValue = (headers: Record<string, string | string[]> | undefined, name: string): string => {
  const raw = headers?.[name];
  if (Array.isArray(raw)) {
    return raw[0] ?? '';
  }
  return raw ?? '';
};

export const assertStatus = (interception: TimedInterception, statusCode: number): void => {
  expect(interception.response, 'la petición debe tener respuesta HTTP').to.exist;
  expect(interception.response?.statusCode, 'status HTTP').to.eq(statusCode);
};

export const assertJsonBody = (interception: TimedInterception): void => {
  const contentType = headerValue(interception.response?.headers, 'content-type');
  expect(contentType, 'Content-Type').to.match(/json/i);
  expect(interception.response?.body, 'cuerpo JSON').to.not.equal(undefined);
};

export const assertResponseTime = (interception: TimedInterception, limit = maxResponseMs()): void => {
  const elapsed = Number(headerValue(interception.response?.headers, 'x-e2e-elapsed-ms'));
  expect(elapsed, 'cabecera x-e2e-elapsed-ms').to.be.finite;
  expect(elapsed, `tiempo de respuesta (${elapsed}ms)`).to.be.at.least(0).and.lessThan(limit);
};

export const assertTaskContract = (task: { id?: unknown; title?: unknown; completed?: unknown }): void => {
  expect(task).to.include.keys('id', 'title', 'completed');
  expect(task.id, 'id de tarea').to.be.a('string').and.not.be.empty;
  expect(task.title, 'título de tarea').to.be.a('string').and.not.be.empty;
  expect(task.completed, 'estado completed').to.be.a('boolean');
};

export const assertLoginContract = (body: { access_token?: unknown; token_type?: unknown }): void => {
  expect(body.access_token, 'access_token').to.be.a('string').and.have.length.greaterThan(20);
  expect(String(body.token_type).toLowerCase(), 'token_type').to.eq('bearer');
};
