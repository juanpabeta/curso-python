import { describe, expect, it, vi } from 'vitest';
import { TaskList } from '@/components/TaskList';
import { completedTask, mixedTasks, pendingTask } from '@/tests/fixtures/tasks';
import { screen } from '@/tests/setup/test-utils';
import { render } from '@testing-library/react';

describe('TaskList — comportamiento inicial', () => {
  it('anuncia un estado vacío cuando no hay tareas', () => {
    render(<TaskList tasks={[]} onToggle={vi.fn()} onDelete={vi.fn()} />);

    expect(screen.getByRole('status')).toHaveTextContent('No hay tareas pendientes.');
    expect(screen.queryByRole('list')).not.toBeInTheDocument();
  });

  it('renderiza cada tarea recibida por props', () => {
    render(<TaskList tasks={mixedTasks} onToggle={vi.fn()} onDelete={vi.fn()} />);

    expect(screen.getByRole('list', { name: 'Lista de tareas' })).toBeInTheDocument();
    expect(screen.getAllByRole('listitem')).toHaveLength(mixedTasks.length);
    expect(screen.getByRole('checkbox', { name: pendingTask.title })).not.toBeChecked();
    expect(screen.getByRole('checkbox', { name: completedTask.title })).toBeChecked();
  });

  it('expone botones de eliminación con nombre accesible', () => {
    render(<TaskList tasks={[pendingTask]} onToggle={vi.fn()} onDelete={vi.fn()} />);

    expect(screen.getByRole('button', { name: `Eliminar ${pendingTask.title}` })).toBeInTheDocument();
  });

  it('marca visualmente las tareas completadas', () => {
    render(<TaskList tasks={[completedTask]} onToggle={vi.fn()} onDelete={vi.fn()} />);

    expect(screen.getByRole('listitem')).toHaveClass('task-item--completed');
    expect(screen.getByText(completedTask.title)).toHaveClass('task-title');
  });
});
