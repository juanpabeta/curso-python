interface AlertProps {
  message: string;
  tone?: 'error' | 'success' | 'info';
  announce?: boolean;
}

export const Alert = ({ message, tone = 'info', announce = true }: AlertProps) => {
  if (!message) {
    return null;
  }

  const role = !announce ? undefined : tone === 'error' ? 'alert' : 'status';

  return (
    <p className={`banner banner--${tone}`} role={role}>
      {message}
    </p>
  );
};
