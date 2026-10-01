import { describe, expect, it, vi } from 'vitest';
import { TaskForm } from '@/components/TaskForm';
import { renderWithUser, screen } from '@/tests/setup/test-utils';

describe('TaskForm — interacción del usuario', () => {
  it('escribe un título válido y lo envía con el botón', async () => {
    const onCreateTask = vi.fn();
    const { user } = renderWithUser(<TaskForm onCreateTask={onCreateTask} />);

    await user.type(screen.getByRole('textbox', { name: 'Título de la tarea' }), 'Leer el capítulo 3');
    await user.click(screen.getByRole('button', { name: 'Agregar tarea' }));

    expect(onCreateTask).toHaveBeenCalledTimes(1);
    expect(onCreateTask).toHaveBeenCalledWith('Leer el capítulo 3');
  });

  it('envía el formulario al presionar Enter sobre el campo', async () => {
    const onCreateTask = vi.fn();
    const { user } = renderWithUser(<TaskForm onCreateTask={onCreateTask} />);

    await user.type(
      screen.getByRole('textbox', { name: 'Título de la tarea' }),
      'Resolver ejercicios{Enter}',
    );

    expect(onCreateTask).toHaveBeenCalledWith('Resolver ejercicios');
  });

  it('permite llegar al botón de envío navegando con Tab', async () => {
    const { user } = renderWithUser(<TaskForm onCreateTask={vi.fn()} />);

    await user.tab();
    expect(screen.getByRole('textbox', { name: 'Título de la tarea' })).toHaveFocus();

    await user.tab();
    expect(screen.getByRole('button', { name: 'Agregar tarea' })).toHaveFocus();
  });

  it('no dispara el callback cuando el usuario envía solo espacios', async () => {
    const onCreateTask = vi.fn();
    const { user } = renderWithUser(<TaskForm onCreateTask={onCreateTask} />);

    await user.type(screen.getByRole('textbox', { name: 'Título de la tarea' }), '     ');
    await user.click(screen.getByRole('button', { name: 'Agregar tarea' }));

    expect(onCreateTask).not.toHaveBeenCalled();
  });

  it('permite crear varias tareas en envíos consecutivos', async () => {
    const onCreateTask = vi.fn();
    const { user } = renderWithUser(<TaskForm onCreateTask={onCreateTask} />);
    const input = screen.getByRole('textbox', { name: 'Título de la tarea' });
    const submit = screen.getByRole('button', { name: 'Agregar tarea' });

    await user.type(input, 'Leer el capítulo 3');
    await user.click(submit);
    await user.type(input, 'Practicar SQL');
    await user.click(submit);

    expect(onCreateTask).toHaveBeenCalledTimes(2);
    expect(onCreateTask).toHaveBeenNthCalledWith(1, 'Leer el capítulo 3');
    expect(onCreateTask).toHaveBeenNthCalledWith(2, 'Practicar SQL');
  });
});
