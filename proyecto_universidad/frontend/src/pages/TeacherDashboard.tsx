import { useMemo } from 'react';
import { Link } from 'react-router-dom';

import { Button } from '@/components/ui/Button';
import { DataTable } from '@/components/ui/DataTable';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { useEnrollments } from '@/hooks/useEnrollments';
import { usePeriods } from '@/hooks/usePeriods';
import { useSubjects } from '@/hooks/useSubjects';
import { useUsers } from '@/hooks/useUsers';
import { buildEnrollmentRows } from '@/utils/academicView';

export const TeacherDashboard = () => {
  useDocumentTitle('Panel docente');
  const subjectsQuery = useSubjects();
  const periodsQuery = usePeriods();
  const usersQuery = useUsers();
  const enrollmentsQuery = useEnrollments();

  const rows = useMemo(
    () => buildEnrollmentRows(enrollmentsQuery.enrollments, subjectsQuery.subjects, periodsQuery.periods, usersQuery.users, []),
    [enrollmentsQuery.enrollments, periodsQuery.periods, subjectsQuery.subjects, usersQuery.users],
  );

  const students = usersQuery.users.filter((user) => user.roles.some((role) => role.name === 'Estudiante'));
  const currentPeriod = [...periodsQuery.periods].sort((left, right) => right.end_date.localeCompare(left.end_date))[0];
  const isLoading = [subjectsQuery, periodsQuery, usersQuery, enrollmentsQuery].some((query) => query.isLoading);
  const loadError = [subjectsQuery.error, periodsQuery.error, usersQuery.error, enrollmentsQuery.error].filter(Boolean).join(' ');

  return (
    <section className="page-panel">
      <header className="page-header">
        <div>
          <h2>Panel docente</h2>
          <p>Consulta el catálogo y las inscripciones. Las notas se registran en Calificaciones.</p>
        </div>
        <Link to="/teacher/calificaciones" className="primary-btn inline-link">
          Registrar calificaciones
        </Link>
      </header>

      {isLoading ? <p className="muted-copy">Cargando información académica...</p> : null}
      {loadError ? (
        <div className="stack-form">
          <p className="error-message">{loadError}</p>
          <Button
            variant="secondary"
            onClick={() => {
              void Promise.all([
                subjectsQuery.reload(),
                periodsQuery.reload(),
                usersQuery.reload(),
                enrollmentsQuery.reload(),
              ]);
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
          <h3>Estudiantes</h3>
          <strong>{isLoading ? '…' : students.length}</strong>
        </article>
        <article className="stat-card">
          <h3>Período</h3>
          <strong>{isLoading ? '…' : (currentPeriod?.code ?? '—')}</strong>
        </article>
      </div>

      {!isLoading && !loadError ? (
        <section className="panel-card" aria-labelledby="teacher-enrollments-title">
          <h3 id="teacher-enrollments-title">Inscripciones</h3>
          <DataTable
            caption="Inscripciones visibles para el docente"
            rows={rows}
            getRowId={(row) => row.id}
            emptyMessage="No hay inscripciones registradas."
            columns={[
              { key: 'user', header: 'Estudiante', render: (row) => row.userLabel },
              { key: 'subject', header: 'Materia', render: (row) => row.subjectLabel },
              { key: 'period', header: 'Período', render: (row) => row.periodLabel },
              {
                key: 'status',
                header: 'Estado',
                render: (row) => <span className={`status-badge status-badge--${row.status}`}>{row.statusLabel}</span>,
              },
            ]}
          />
        </section>
      ) : null}

      
    </section>
  );
};
