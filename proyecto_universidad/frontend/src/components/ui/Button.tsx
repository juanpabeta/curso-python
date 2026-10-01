import type { ButtonHTMLAttributes, ReactNode } from 'react';

type ButtonVariant = 'primary' | 'secondary' | 'danger';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  isLoading?: boolean;
  loadingLabel?: string;
  children: ReactNode;
}

export const Button = ({
  variant = 'primary',
  isLoading = false,
  loadingLabel = 'Procesando...',
  children,
  className = '',
  disabled,
  type = 'button',
  ...props
}: ButtonProps) => {
  const classes = ['ui-btn', `ui-btn--${variant}`, className].filter(Boolean).join(' ');

  return (
    <button
      {...props}
      type={type}
      className={classes}
      disabled={disabled || isLoading}
      aria-busy={isLoading || undefined}
    >
      {isLoading ? loadingLabel : children}
    </button>
  );
};
