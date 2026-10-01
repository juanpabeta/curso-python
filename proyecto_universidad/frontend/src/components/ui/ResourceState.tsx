import type { ReactNode } from 'react';

interface ResourceStateProps {
  isLoading: boolean;
  error: string;
  isEmpty?: boolean;
  emptyMessage?: string;
  announce?: boolean;
  children: ReactNode;
}

export const ResourceState = ({
  isLoading,
  error,
  isEmpty = false,
  emptyMessage = 'No hay registros para mostrar.',
  announce = false,
  children,
}: ResourceStateProps) => {
  if (isLoading) {
    return (
      <p className="muted-copy" role={announce ? 'status' : undefined}>
        Cargando información...
      </p>
    );
  }

  if (error) {
    return (
      <p className="error-message" role={announce ? 'alert' : undefined}>
        {error}
      </p>
    );
  }

  if (isEmpty) {
    return <p className="muted-copy">{emptyMessage}</p>;
  }

  return children;
};
