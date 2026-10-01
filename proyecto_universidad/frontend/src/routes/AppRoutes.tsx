import { Navigate, Route, Routes } from 'react-router-dom';
import { ProtectedRoute } from '@/auth/ProtectedRoute';
import { DashboardLayout } from '@/layouts/DashboardLayout';
import { AuthLayout } from '@/layouts/AuthLayout';
import { EnrollmentsPage } from '@/pages/admin/EnrollmentsPage';
import { PeriodsPage } from '@/pages/admin/PeriodsPage';
import { SubjectsPage } from '@/pages/admin/SubjectsPage';
import { UsersPage } from '@/pages/admin/UsersPage';
import { AdminDashboard } from '@/pages/AdminDashboard';
import { GradesPage } from '@/pages/GradesPage';
import { LoginPage } from '@/pages/LoginPage';
import { NotFoundPage } from '@/pages/NotFoundPage';
import { ServerErrorPage } from '@/pages/ServerErrorPage';
import { StudentDashboard } from '@/pages/StudentDashboard';
import { TeacherDashboard } from '@/pages/TeacherDashboard';
import { UnauthorizedPage } from '@/pages/UnauthorizedPage';
import { useAuth } from '@/hooks/useAuth';

const HomeRedirect = () => {
  const { user } = useAuth();

  if (user?.roles.includes('Administrador')) {
    return <Navigate to="/admin" replace />;
  }

  if (user?.roles.includes('Docente')) {
    return <Navigate to="/teacher" replace />;
  }

  if (user?.roles.includes('Estudiante')) {
    return <Navigate to="/student" replace />;
  }

  return <Navigate to="/login" replace />;
};

export const AppRoutes = () => {
  return (
    <Routes>
      <Route element={<AuthLayout />}>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/unauthorized" element={<UnauthorizedPage />} />
        <Route path="/404" element={<NotFoundPage />} />
        <Route path="/error" element={<ServerErrorPage />} />
      </Route>

      <Route
        element={
          <ProtectedRoute>
            <DashboardLayout />
          </ProtectedRoute>
        }
      >
        <Route path="/" element={<HomeRedirect />} />
        <Route
          path="/student"
          element={
            <ProtectedRoute allowedRoles={['Estudiante']}>
              <StudentDashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/teacher"
          element={
            <ProtectedRoute allowedRoles={['Docente']}>
              <TeacherDashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/teacher/calificaciones"
          element={
            <ProtectedRoute allowedRoles={['Docente']}>
              <GradesPage
                title="Calificaciones"
                description="Registra y corrige notas. La baja de una calificación queda reservada a administración."
              />
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin"
          element={
            <ProtectedRoute allowedRoles={['Administrador']}>
              <AdminDashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/materias"
          element={
            <ProtectedRoute allowedRoles={['Administrador']}>
              <SubjectsPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/usuarios"
          element={
            <ProtectedRoute allowedRoles={['Administrador']}>
              <UsersPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/periodos"
          element={
            <ProtectedRoute allowedRoles={['Administrador']}>
              <PeriodsPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/inscripciones"
          element={
            <ProtectedRoute allowedRoles={['Administrador']}>
              <EnrollmentsPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/calificaciones"
          element={
            <ProtectedRoute allowedRoles={['Administrador']}>
              <GradesPage allowDelete description="Consulta, registra, corrige y elimina calificaciones." />
            </ProtectedRoute>
          }
        />
      </Route>

      <Route path="*" element={<Navigate to="/404" replace />} />
    </Routes>
  );
};
