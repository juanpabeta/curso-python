import { FormEvent, useState } from 'react';
import { sanitizeText } from '@/utils/sanitize';
import { TASK_TITLE_MAX_LENGTH, validateTaskTitle } from '@/utils/validators';

export interface TaskFormProps {
  onCreateTask: (title: string) => void | Promise<void>;
  isSubmitting?: boolean;
  maxLength?: number;
}

export const TaskForm = ({
  onCreateTask,
  isSubmitting = false,
  maxLength = TASK_TITLE_MAX_LENGTH,
}: TaskFormProps) => {
  const [title, setTitle] = useState('');
  const [error, setError] = useState('');
  const [isPending, setIsPending] = useState(false);

  const submitting = isSubmitting || isPending;
  const hintId = 'task-title-hint';
  const errorId = 'task-title-error';

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const validationError = validateTaskTitle(title, maxLength);
    if (validationError) {
      setError(validationError);
      return;
    }

    setError('');
    setIsPending(true);

    try {
      await onCreateTask(sanitizeText(title));
      setTitle('');
    } catch {
      setError('No se pudo crear la tarea. Inténtalo de nuevo.');
    } finally {
      setIsPending(false);
    }
  };

  return (
    <form aria-label="Crear tarea" onSubmit={(event) => void handleSubmit(event)} noValidate>
      <label htmlFor="task-title">Título de la tarea</label>
      <div className="task-form-row">
        <input
          id="task-title"
          type="text"
          value={title}
          onChange={(event) => {
            setTitle(event.target.value);
            if (error) {
              setError('');
            }
          }}
          placeholder="Ej. Leer el capítulo 3"
          autoComplete="off"
          disabled={submitting}
          aria-invalid={Boolean(error)}
          aria-describedby={error ? `${hintId} ${errorId}` : hintId}
        />
        <button type="submit" className="primary-btn" disabled={submitting}>
          {submitting ? 'Agregando...' : 'Agregar tarea'}
        </button>
      </div>
      <p id={hintId} className="task-hint">
        {title.trim().length}/{maxLength} caracteres
      </p>
      {error ? (
        <p id={errorId} className="error-message" role="alert">
          {error}
        </p>
      ) : null}
    </form>
  );
};
