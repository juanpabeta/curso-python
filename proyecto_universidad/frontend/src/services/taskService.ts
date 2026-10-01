import { api } from '@/api/client';
import type { Task } from '@/types';

const isTask = (value: unknown): value is Task => {
  if (!value || typeof value !== 'object') {
    return false;
  }

  const task = value as Partial<Task>;
  return typeof task.id === 'string' && typeof task.title === 'string' && typeof task.completed === 'boolean';
};

const assertTask = (value: unknown): Task => {
  if (!isTask(value)) {
    throw new Error('La respuesta de tarea no cumple el contrato JSON.');
  }
  return value;
};

const assertTaskList = (value: unknown): Task[] => {
  if (!Array.isArray(value) || value.some((item) => !isTask(item))) {
    throw new Error('La respuesta de tareas no cumple el contrato JSON.');
  }
  return value;
};

export const resetTaskStore = (_tasks: Task[] = []): void => {
  // La persistencia real se limpia desde la API en la suite E2E.
};

export const fetchTasks = async (): Promise<Task[]> => {
  const response = await api.get<unknown>('/tasks/');
  return assertTaskList(response.data);
};

export const createTask = async (title: string): Promise<Task> => {
  const response = await api.post<unknown>('/tasks/', { title });
  return assertTask(response.data);
};

export const toggleTask = async (id: string): Promise<Task> => {
  const response = await api.post<unknown>(`/tasks/${id}/toggle`);
  return assertTask(response.data);
};

export const deleteTask = async (id: string): Promise<void> => {
  await api.delete(`/tasks/${id}`);
};
