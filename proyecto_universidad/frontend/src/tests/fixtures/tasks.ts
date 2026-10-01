import type { Task } from '@/types';

export const pendingTask: Task = {
  id: 'task-1',
  title: 'Leer el capítulo 3',
  completed: false,
};

export const completedTask: Task = {
  id: 'task-2',
  title: 'Entregar el ensayo',
  completed: true,
};

export const extraTask: Task = {
  id: 'task-3',
  title: 'Practicar consultas SQL',
  completed: false,
};

export const mixedTasks: Task[] = [pendingTask, completedTask, extraTask];

export const longTaskTitle = 'Preparar la exposición de diseño de software '.repeat(4).trim();
