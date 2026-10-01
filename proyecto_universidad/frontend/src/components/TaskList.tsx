import type { Task } from '@/types';

export interface TaskListProps {
  tasks: Task[];
  onToggle: (id: string) => void | Promise<void>;
  onDelete: (id: string) => void | Promise<void>;
}

export const TaskList = ({ tasks, onToggle, onDelete }: TaskListProps) => {
  if (tasks.length === 0) {
    return (
      <p className="task-empty" role="status">
        No hay tareas pendientes.
      </p>
    );
  }

  return (
    <ul className="task-list" aria-label="Lista de tareas">
      {tasks.map((task) => (
        <li key={task.id} className={task.completed ? 'task-item task-item--completed' : 'task-item'}>
          <label className="task-toggle">
            <input
              type="checkbox"
              checked={task.completed}
              onChange={() => void onToggle(task.id)}
            />
            <span className="task-title">{task.title}</span>
          </label>
          <button
            type="button"
            className="danger-btn"
            aria-label={`Eliminar ${task.title}`}
            onClick={() => void onDelete(task.id)}
          >
            Eliminar
          </button>
        </li>
      ))}
    </ul>
  );
};
