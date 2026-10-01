import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/Button';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { useEnrollments } from '@/hooks/useEnrollments';
import { useSubjects } from '@/hooks/useSubjects';
import { useUsers } from '@/hooks/useUsers';

const QUICK_LINKS = [
  { to: '/admin/materias', label: 'Materias', text: 'Crear y editar el catálogo' },
  { to: '/admin/usuarios', label: 'Usuarios', text: 'Cuentas, roles y acceso' },
  { to: '/admin/periodos', label: 'Períodos', text: 'Calendario académico' },
  { to: '/admin/inscripciones', label: 'Inscripciones', text: 'Matrícula de estudiantes' },
  { to: '/admin/calificaciones', label: 'Calificaciones', text: 'Notas y comentarios' },
];

export const AdminDashboard = () => {
  useDocumentTitle('Panel administrador');
  const subjectsQuery = useSubjects();
  const usersQuery = useUsers();
  const enrollmentsQuery = useEnrollments();
  const isLoading = subjectsQuery.isLoading || usersQuery.isLoading || enrollmentsQuery.isLoading;
  const loadError = [subjectsQuery.error, usersQuery.error, enrollmentsQuery.error].filter(Boolean).join(' ');

  return (
    <section className="page-panel">
      <header>
        <h2>Panel administrador</h2>
        <p>Gestión académica conectada a la API.</p>
      </header>

      {isLoading ? <p className="muted-copy">Cargando indicadores...</p> : null}
      {loadError ? (
        <div className="stack-form">
          <p className="error-message">{loadError}</p>
          <Button
            variant="secondary"
            onClick={() => {
              void Promise.all([subjectsQuery.reload(), usersQuery.reload(), enrollmentsQuery.reload()]);
            }}
          >
            Reintentar
          </Button>
        </div>
      ) : null}

      <div className="stats-grid">
        <article className="stat-card">
          <h3>Materias</h3>
          <strong>{isLoading ? '…' : subjectsQuery.subjects.length}</strong>
        </article>
        <article className="stat-card">
          <h3>Usuarios</h3>
          <strong>{isLoading ? '…' : usersQuery.users.length}</strong>
        </article>
        <article className="stat-card">
          <h3>Inscripciones</h3>
          <strong>{isLoading ? '…' : enrollmentsQuery.enrollments.length}</strong>
        </article>
      </div>

      <nav className="quick-links" aria-label="Gestión académica">
        {QUICK_LINKS.map((link) => (
          <Link key={link.to} to={link.to} className="quick-link">
            <strong>{link.label}</strong>
            <span>{link.text}</span>
          </Link>
        ))}
      </nav>

     
    </section>
  );
};
