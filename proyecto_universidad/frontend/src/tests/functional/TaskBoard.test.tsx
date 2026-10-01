import { beforeEach, describe, expect, it, vi } from 'vitest';
import { TaskBoard } from '@/components/TaskBoard';
import { createTask, deleteTask, fetchTasks, toggleTask } from '@/services/taskService';
import { mixedTasks, pendingTask } from '@/tests/fixtures/tasks';
import { renderWithUser, screen, waitFor } from '@/tests/setup/test-utils';

vi.mock('@/services/taskService', () => ({
  fetchTasks: vi.fn(),
  createTask: vi.fn(),
  toggleTask: vi.fn(),
  deleteTask: vi.fn(),
}));

describe('TaskBoard — flujo funcional local', () => {
  it('agrega la tarea escrita a la lista visible', async () => {
    const { user } = renderWithUser(<TaskBoard />);

    await user.type(
      screen.getByRole('textbox', { name: 'Título de la tarea' }),
      'Repasar normalización',
    );
    await user.click(screen.getByRole('button', { name: 'Agregar tarea' }));

    expect(await screen.findByRole('checkbox', { name: 'Repasar normalización' })).toBeInTheDocument();
    expect(screen.getByRole('textbox', { name: 'Título de la tarea' })).toHaveValue('');
  });

  it('marca una tarea como completada y cambia su estilo', async () => {
    const { user } = renderWithUser(<TaskBoard initialTasks={[pendingTask]} />);

    await user.click(screen.getByRole('checkbox', { name: pendingTask.title }));

    expect(screen.getByRole('checkbox', { name: pendingTask.title })).toBeChecked();
    expect(screen.getByRole('listitem')).toHaveClass('task-item--completed');
  });

  it('elimina una tarea de la lista y muestra el estado vacío', async () => {
    const { user } = renderWithUser(<TaskBoard initialTasks={[pendingTask]} />);

    await user.click(screen.getByRole('button', { name: `Eliminar ${pendingTask.title}` }));

    expect(screen.getByRole('status')).toHaveTextContent('No hay tareas pendientes.');
    expect(screen.queryByRole('checkbox', { name: pendingTask.title })).not.toBeInTheDocument();
  });
});

describe('TaskBoard — datos de servidor simulados', () => {
  beforeEach(() => {
    vi.mocked(fetchTasks).mockReset();
    vi.mocked(createTask).mockReset();
    vi.mocked(toggleTask).mockReset();
    vi.mocked(deleteTask).mockReset();
  });

  it('muestra las tareas que llegan desde el servidor', async () => {
    vi.mocked(fetchTasks).mockResolvedValue(mixedTasks);

    renderWithUser(<TaskBoard useRemoteSource />);

    expect(screen.getByRole('status')).toHaveTextContent('Cargando tareas...');
    expect(await screen.findByRole('list', { name: 'Lista de tareas' })).toBeInTheDocument();
    expect(screen.getAllByRole('listitem')).toHaveLength(mixedTasks.length);
  });

  it('crea una tarea contra el servicio simulado y la pinta en la UI', async () => {
    vi.mocked(fetchTasks).mockResolvedValue([]);
    vi.mocked(createTask).mockResolvedValue({
      id: 'server-1',
      title: 'Estudiar para el parcial',
      completed: false,
    });

    const { user } = renderWithUser(<TaskBoard useRemoteSource />);
    expect(await screen.findByText('No hay tareas pendientes.')).toBeInTheDocument();

    await user.type(
      screen.getByRole('textbox', { name: 'Título de la tarea' }),
      'Estudiar para el parcial',
    );
    await user.click(screen.getByRole('button', { name: 'Agregar tarea' }));

    await waitFor(() => {
      expect(createTask).toHaveBeenCalledWith('Estudiar para el parcial');
    });
    expect(await screen.findByRole('checkbox', { name: 'Estudiar para el parcial' })).toBeInTheDocument();
  });

  it('deshabilita el botón mientras el servidor tarda en crear la tarea', async () => {
    vi.mocked(fetchTasks).mockResolvedValue([]);
    let resolveCreate: ((task: { id: string; title: string; completed: boolean }) => void) | undefined;
    vi.mocked(createTask).mockImplementation(
      () =>
        new Promise((resolve) => {
          resolveCreate = resolve;
        }),
    );

    const { user } = renderWithUser(<TaskBoard useRemoteSource />);
    await screen.findByText('No hay tareas pendientes.');

    await user.type(screen.getByRole('textbox', { name: 'Título de la tarea' }), 'Tarea lenta');
    await user.click(screen.getByRole('button', { name: 'Agregar tarea' }));

    expect(screen.getByRole('button', { name: 'Agregando...' })).toBeDisabled();

    resolveCreate?.({ id: 'slow-1', title: 'Tarea lenta', completed: false });

    await waitFor(() => {
      expect(screen.getByRole('button', { name: 'Agregar tarea' })).toBeEnabled();
    });
  });

  it('avisa cuando el servidor no puede cargar las tareas', async () => {
    vi.mocked(fetchTasks).mockRejectedValue(new Error('offline'));

    renderWithUser(<TaskBoard useRemoteSource />);

    expect(await screen.findByRole('alert')).toHaveTextContent('No se pudieron cargar las tareas.');
  });

  it('sincroniza toggle y borrado con el servicio simulado', async () => {
    vi.mocked(fetchTasks).mockResolvedValue([pendingTask]);
    vi.mocked(toggleTask).mockResolvedValue({ ...pendingTask, completed: true });
    vi.mocked(deleteTask).mockResolvedValue(undefined);

    const { user } = renderWithUser(<TaskBoard useRemoteSource />);
    await screen.findByRole('checkbox', { name: pendingTask.title });

    await user.click(screen.getByRole('checkbox', { name: pendingTask.title }));
    await waitFor(() => {
      expect(toggleTask).toHaveBeenCalledWith(pendingTask.id);
    });
    expect(screen.getByRole('listitem')).toHaveClass('task-item--completed');

    await user.click(screen.getByRole('button', { name: `Eliminar ${pendingTask.title}` }));
    await waitFor(() => {
      expect(deleteTask).toHaveBeenCalledWith(pendingTask.id);
    });
    expect(screen.getByRole('status')).toHaveTextContent('No hay tareas pendientes.');
  });
});
