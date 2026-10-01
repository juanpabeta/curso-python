import { describe, expect, it, vi } from 'vitest';
import { TaskList } from '@/components/TaskList';
import { mixedTasks, pendingTask } from '@/tests/fixtures/tasks';
import { renderWithUser, screen } from '@/tests/setup/test-utils';

describe('TaskList — interacción del usuario', () => {
  it('marca una tarea como completada al activar su checkbox', async () => {
    const onToggle = vi.fn();
    const { user } = renderWithUser(
      <TaskList tasks={mixedTasks} onToggle={onToggle} onDelete={vi.fn()} />,
    );

    await user.click(screen.getByRole('checkbox', { name: pendingTask.title }));

    expect(onToggle).toHaveBeenCalledTimes(1);
    expect(onToggle).toHaveBeenCalledWith(pendingTask.id);
  });

  it('elimina una tarea al pulsar su botón accesible', async () => {
    const onDelete = vi.fn();
    const { user } = renderWithUser(
      <TaskList tasks={mixedTasks} onToggle={vi.fn()} onDelete={onDelete} />,
    );

    await user.click(screen.getByRole('button', { name: `Eliminar ${pendingTask.title}` }));

    expect(onDelete).toHaveBeenCalledWith(pendingTask.id);
  });

  it('alterna el checkbox con la barra espaciadora', async () => {
    const onToggle = vi.fn();
    const { user } = renderWithUser(
      <TaskList tasks={[pendingTask]} onToggle={onToggle} onDelete={vi.fn()} />,
    );

    screen.getByRole('checkbox', { name: pendingTask.title }).focus();
    await user.keyboard(' ');

    expect(onToggle).toHaveBeenCalledWith(pendingTask.id);
  });

  it('activa eliminar con Enter cuando el botón tiene el foco', async () => {
    const onDelete = vi.fn();
    const { user } = renderWithUser(
      <TaskList tasks={[pendingTask]} onToggle={vi.fn()} onDelete={onDelete} />,
    );

    screen.getByRole('button', { name: `Eliminar ${pendingTask.title}` }).focus();
    await user.keyboard('{Enter}');

    expect(onDelete).toHaveBeenCalledWith(pendingTask.id);
  });
});
