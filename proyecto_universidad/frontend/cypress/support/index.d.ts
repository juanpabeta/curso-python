export {};

declare global {
  type AcademicUserKey = 'student' | 'admin' | 'teacher' | 'invalid';

  interface AcademicUser {
    email: string;
    password: string;
    fullName: string;
    role: 'Administrador' | 'Docente' | 'Estudiante';
    dashboardPath: string;
    dashboardHeading: string;
  }

  interface AcademicTask {
    id: string;
    title: string;
    completed: boolean;
  }

  namespace Cypress {
    interface Chainable {
      getFixtureUser(key?: AcademicUserKey): Chainable<AcademicUser>;
      loginByUi(user?: AcademicUserKey | AcademicUser): Chainable<void>;
      loginByApi(user?: AcademicUserKey | AcademicUser): Chainable<string>;
      ensureSession(user?: AcademicUserKey): Chainable<void>;
      logoutByUi(): Chainable<void>;
      clearClientState(): Chainable<void>;
      ensureAcademicUsers(): Chainable<void>;
      createTaskByApi(title: string, token?: string): Chainable<AcademicTask>;
      listTasksByApi(token?: string): Chainable<AcademicTask[]>;
      deleteTaskByApi(id: string, token?: string): Chainable<void>;
      deleteTasksByTitlePrefix(prefix: string, token?: string): Chainable<void>;
      spyAuthApi(): Chainable<void>;
      spyTasksApi(): Chainable<void>;
      stubLoginNetworkError(): Chainable<void>;
      stubLoginServerDown(): Chainable<void>;
      stubCreateTaskError(statusCode?: number): Chainable<void>;
      stubCreateTaskDelay(delayMs?: number, body?: AcademicTask): Chainable<void>;
      stubCreateTaskOffline(): Chainable<void>;
      stubTasksCorrupt(): Chainable<void>;
      stubTasksPartialCreate(): Chainable<void>;
      stubTasksTimeout(): Chainable<void>;
    }
  }
}
