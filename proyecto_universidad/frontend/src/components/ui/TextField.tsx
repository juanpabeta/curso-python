import type { InputHTMLAttributes } from 'react';

interface TextFieldProps extends Omit<InputHTMLAttributes<HTMLInputElement | HTMLTextAreaElement>, 'onChange' | 'value'> {
  id: string;
  label: string;
  value: string;
  onChange: (value: string) => void;
  error?: string;
  hint?: string;
  multiline?: boolean;
  invalid?: boolean;
}

export const TextField = ({
  id,
  label,
  value,
  onChange,
  error,
  hint,
  multiline = false,
  invalid = false,
  required,
  type = 'text',
  ...props
}: TextFieldProps) => {
  const hintId = hint ? `${id}-hint` : undefined;
  const errorId = error ? `${id}-error` : undefined;
  const describedBy = [hintId, errorId].filter(Boolean).join(' ') || undefined;
  const shared = {
    id,
    value,
    required,
    'aria-required': required || undefined,
    'aria-invalid': Boolean(error) || invalid || undefined,
    'aria-describedby': describedBy,
    onChange: (event: { target: { value: string } }) => onChange(event.target.value),
  };

  return (
    <div className="field">
      <label htmlFor={id}>{label}</label>
      {multiline ? (
        <textarea {...props} {...shared} rows={4} />
      ) : (
        <input {...props} {...shared} type={type} />
      )}
      {hint ? (
        <p id={hintId} className="field-hint">
          {hint}
        </p>
      ) : null}
      {error ? (
        <p id={errorId} className="field-error">
          {error}
        </p>
      ) : null}
    </div>
  );
};
