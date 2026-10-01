import type { ReactElement } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '@/hooks/useAuth';
import type { RoleName } from '@/types';

interface ProtectedRouteProps {
  allowedRoles?: RoleName[];
  children: ReactElement;
}

export const ProtectedRoute = ({ allowedRoles = [], children }: ProtectedRouteProps) => {
  const { isAuthenticated, user, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) {
    return (
      <p role="status" className="task-empty">
        Cargando sesión...
      </p>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace state={{ from: location }} />;
  }

  if (allowedRoles.length > 0 && (!user || !allowedRoles.some((role) => user.roles.includes(role)))) {
    return <Navigate to="/unauthorized" replace />;
  }

  return children;
};
