import { describe, expect, it, vi } from 'vitest';
import { TaskList } from '@/components/TaskList';
import { extraTask, mixedTasks, pendingTask } from '@/tests/fixtures/tasks';
import { screen } from '@/tests/setup/test-utils';
import { render } from '@testing-library/react';

describe('TaskList — cambios de interfaz', () => {
  it('actualiza el estilo completado cuando el padre re-renderiza la tarea', () => {
    const { rerender } = render(
      <TaskList tasks={[pendingTask]} onToggle={vi.fn()} onDelete={vi.fn()} />,
    );

    expect(screen.getByRole('checkbox', { name: pendingTask.title })).not.toBeChecked();
    expect(screen.getByRole('listitem')).not.toHaveClass('task-item--completed');

    rerender(
      <TaskList
        tasks={[{ ...pendingTask, completed: true }]}
        onToggle={vi.fn()}
        onDelete={vi.fn()}
      />,
    );

    expect(screen.getByRole('checkbox', { name: pendingTask.title })).toBeChecked();
    expect(screen.getByRole('listitem')).toHaveClass('task-item--completed');
  });

  it('vuelve al estado vacío cuando el padre deja de enviar tareas', () => {
    const { rerender } = render(
      <TaskList tasks={mixedTasks} onToggle={vi.fn()} onDelete={vi.fn()} />,
    );

    expect(screen.getAllByRole('listitem')).toHaveLength(mixedTasks.length);

    rerender(<TaskList tasks={[]} onToggle={vi.fn()} onDelete={vi.fn()} />);

    expect(screen.getByRole('status')).toHaveTextContent('No hay tareas pendientes.');
    expect(screen.queryByRole('list')).not.toBeInTheDocument();
  });

  it('incorpora nuevas tareas al re-renderizar con más elementos', () => {
    const { rerender } = render(
      <TaskList tasks={[pendingTask]} onToggle={vi.fn()} onDelete={vi.fn()} />,
    );

    rerender(
      <TaskList tasks={[pendingTask, extraTask]} onToggle={vi.fn()} onDelete={vi.fn()} />,
    );

    expect(screen.getAllByRole('listitem')).toHaveLength(2);
    expect(screen.getByRole('checkbox', { name: extraTask.title })).toBeInTheDocument();
  });
});
