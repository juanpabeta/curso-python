import { useEffect, useState } from 'react';
import { TaskForm } from '@/components/TaskForm';
import { TaskList } from '@/components/TaskList';
import { createTask, deleteTask, fetchTasks, toggleTask } from '@/services/taskService';
import type { Task } from '@/types';

export interface TaskBoardProps {
  initialTasks?: Task[];
  useRemoteSource?: boolean;
  heading?: string;
}

export const TaskBoard = ({
  initialTasks = [],
  useRemoteSource = false,
  heading = 'Tareas académicas',
}: TaskBoardProps) => {
  const [tasks, setTasks] = useState<Task[]>(initialTasks);
  const [isLoading, setIsLoading] = useState(useRemoteSource);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [loadError, setLoadError] = useState('');
  const [actionError, setActionError] = useState('');

  useEffect(() => {
    if (!useRemoteSource) {
      return;
    }

    let cancelled = false;
    setIsLoading(true);
    setLoadError('');

    fetchTasks()
      .then((data) => {
        if (!cancelled) {
          setTasks(data);
        }
      })
      .catch(() => {
        if (!cancelled) {
          setLoadError('No se pudieron cargar las tareas.');
        }
      })
      .finally(() => {
        if (!cancelled) {
          setIsLoading(false);
        }
      });

    return () => {
      cancelled = true;
    };
  }, [useRemoteSource]);

  const handleCreate = async (title: string) => {
    setIsSubmitting(true);
    setActionError('');

    try {
      if (useRemoteSource) {
        const created = await createTask(title);
        setTasks((current) => [...current, created]);
        return;
      }

      setTasks((current) => [
        ...current,
        { id: crypto.randomUUID(), title, completed: false },
      ]);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleToggle = async (id: string) => {
    setActionError('');

    try {
      if (useRemoteSource) {
        const updated = await toggleTask(id);
        setTasks((current) => current.map((task) => (task.id === id ? updated : task)));
        return;
      }

      setTasks((current) =>
        current.map((task) => (task.id === id ? { ...task, completed: !task.completed } : task)),
      );
    } catch {
      setActionError('No se pudo actualizar la tarea.');
    }
  };

  const handleDelete = async (id: string) => {
    setActionError('');

    try {
      if (useRemoteSource) {
        await deleteTask(id);
      }

      setTasks((current) => current.filter((task) => task.id !== id));
    } catch {
      setActionError('No se pudo eliminar la tarea.');
    }
  };

  return (
    <section className="task-board" aria-labelledby="task-board-title">
      <h3 id="task-board-title">{heading}</h3>
      <TaskForm onCreateTask={handleCreate} isSubmitting={isSubmitting} />
      {actionError ? (
        <p className="error-message" role="alert">
          {actionError}
        </p>
      ) : null}
      {isLoading ? (
        <p role="status">Cargando tareas...</p>
      ) : loadError ? (
        <p className="error-message" role="alert">
          {loadError}
        </p>
      ) : (
        <TaskList tasks={tasks} onToggle={handleToggle} onDelete={handleDelete} />
      )}
    </section>
  );
};
