import { describe, expect, it, vi } from 'vitest';
import { TaskForm } from '@/components/TaskForm';
import { longTaskTitle } from '@/tests/fixtures/tasks';
import { renderWithUser, screen, waitFor } from '@/tests/setup/test-utils';

describe('TaskForm — cambios de interfaz', () => {
  it('muestra un error accesible cuando el título está vacío', async () => {
    const onCreateTask = vi.fn();
    const { user } = renderWithUser(<TaskForm onCreateTask={onCreateTask} />);

    await user.click(screen.getByRole('button', { name: 'Agregar tarea' }));

    expect(screen.getByRole('alert')).toHaveTextContent('Escribe el título de la tarea.');
    expect(screen.getByRole('textbox', { name: 'Título de la tarea' })).toHaveAttribute(
      'aria-invalid',
      'true',
    );
    expect(onCreateTask).not.toHaveBeenCalled();
  });

  it('limpia el campo después de crear una tarea válida', async () => {
    const { user } = renderWithUser(<TaskForm onCreateTask={vi.fn()} />);
    const input = screen.getByRole('textbox', { name: 'Título de la tarea' });

    await user.type(input, 'Estudiar algoritmos');
    await user.click(screen.getByRole('button', { name: 'Agregar tarea' }));

    await waitFor(() => {
      expect(input).toHaveValue('');
    });
    expect(screen.queryByRole('alert')).not.toBeInTheDocument();
  });

  it('rechaza un título que supera el máximo de caracteres', async () => {
    const onCreateTask = vi.fn();
    const { user } = renderWithUser(<TaskForm onCreateTask={onCreateTask} />);
    const input = screen.getByRole('textbox', { name: 'Título de la tarea' });

    await user.click(input);
    await user.paste(longTaskTitle);
    await user.click(screen.getByRole('button', { name: 'Agregar tarea' }));

    expect(screen.getByRole('alert')).toHaveTextContent('El título no puede superar 120 caracteres.');
    expect(onCreateTask).not.toHaveBeenCalled();
    expect(input).toHaveValue(longTaskTitle);
  });

  it('deshabilita el envío mientras la creación asíncrona está en curso', async () => {
    let resolveCreate: (() => void) | undefined;
    const onCreateTask = vi.fn(
      () =>
        new Promise<void>((resolve) => {
          resolveCreate = resolve;
        }),
    );
    const { user } = renderWithUser(<TaskForm onCreateTask={onCreateTask} />);

    await user.type(screen.getByRole('textbox', { name: 'Título de la tarea' }), 'Nueva tarea');
    await user.click(screen.getByRole('button', { name: 'Agregar tarea' }));

    const busyButton = screen.getByRole('button', { name: 'Agregando...' });
    expect(busyButton).toBeDisabled();
    expect(screen.getByRole('textbox', { name: 'Título de la tarea' })).toBeDisabled();

    resolveCreate?.();

    await waitFor(() => {
      expect(screen.getByRole('button', { name: 'Agregar tarea' })).toBeEnabled();
    });
  });

  it('conserva el texto y avisa si el servidor rechaza la creación', async () => {
    const onCreateTask = vi.fn().mockRejectedValue(new Error('network'));
    const { user } = renderWithUser(<TaskForm onCreateTask={onCreateTask} />);
    const input = screen.getByRole('textbox', { name: 'Título de la tarea' });

    await user.type(input, 'Tarea que falla');
    await user.click(screen.getByRole('button', { name: 'Agregar tarea' }));

    expect(await screen.findByRole('alert')).toHaveTextContent('No se pudo crear la tarea. Inténtalo de nuevo.');
    expect(input).toHaveValue('Tarea que falla');
  });
});
