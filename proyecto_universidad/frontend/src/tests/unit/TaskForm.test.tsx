import { describe, expect, it, vi } from 'vitest';
import { TaskForm } from '@/components/TaskForm';
import { screen } from '@/tests/setup/test-utils';
import { render } from '@testing-library/react';

describe('TaskForm — comportamiento inicial', () => {
  it('muestra el campo etiquetado y el botón de envío al renderizar', () => {
    render(<TaskForm onCreateTask={vi.fn()} />);

    expect(screen.getByRole('form', { name: 'Crear tarea' })).toBeInTheDocument();
    expect(screen.getByRole('textbox', { name: 'Título de la tarea' })).toBeEnabled();
    expect(screen.getByRole('button', { name: 'Agregar tarea' })).toBeEnabled();
  });

  it('asocia el label con el input para lectores de pantalla', () => {
    render(<TaskForm onCreateTask={vi.fn()} />);

    expect(screen.getByLabelText('Título de la tarea')).toHaveAttribute('id', 'task-title');
  });

  it('no muestra un error de validación antes de interactuar', () => {
    render(<TaskForm onCreateTask={vi.fn()} />);

    expect(screen.queryByRole('alert')).not.toBeInTheDocument();
    expect(screen.getByRole('textbox', { name: 'Título de la tarea' })).toHaveAttribute(
      'aria-invalid',
      'false',
    );
  });

  it('informa el límite de caracteres con texto visible', () => {
    render(<TaskForm onCreateTask={vi.fn()} maxLength={120} />);

    expect(screen.getByText('0/120 caracteres')).toBeInTheDocument();
  });
});
