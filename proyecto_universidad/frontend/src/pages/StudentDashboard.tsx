import { useMemo } from 'react';
import { TaskBoard } from '@/components/TaskBoard';
import { Button } from '@/components/ui/Button';
import { DataTable } from '@/components/ui/DataTable';
import { useAuth } from '@/hooks/useAuth';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { useEnrollments } from '@/hooks/useEnrollments';
import { useGrades } from '@/hooks/useGrades';
import { usePeriods } from '@/hooks/usePeriods';
import { useSubjects } from '@/hooks/useSubjects';
import { StudentEnrollmentForm } from '@/pages/student/StudentEnrollmentForm';
import type { UserRecord } from '@/types';
import { averageScore, buildEnrollmentRows, describeStudentStatus, formatScore } from '@/utils/academicView';

export const StudentDashboard = () => {
  useDocumentTitle('Panel del estudiante');
  const { user } = useAuth();
  const subjectsQuery = useSubjects();
  const periodsQuery = usePeriods();
  const enrollmentsQuery = useEnrollments();
  const gradesQuery = useGrades();

  const sessionUser = useMemo<UserRecord[]>(() => {
    if (!user) {
      return [];
    }
    return [
      {
        id: user.id,
        email: user.email,
        full_name: user.full_name,
        is_active: true,
        is_superuser: false,
        roles: [],
      },
    ];
  }, [user]);

  const ownRows = useMemo(() => {
    const ownEnrollments = enrollmentsQuery.enrollments.filter((enrollment) => enrollment.user_id === user?.id);
    const ownIds = new Set(ownEnrollments.map((enrollment) => enrollment.id));
    const ownGrades = gradesQuery.grades.filter((grade) => ownIds.has(grade.enrollment_id));
    return buildEnrollmentRows(ownEnrollments, subjectsQuery.subjects, periodsQuery.periods, sessionUser, ownGrades);
  }, [enrollmentsQuery.enrollments, gradesQuery.grades, periodsQuery.periods, sessionUser, subjectsQuery.subjects, user?.id]);

  const status = describeStudentStatus(ownRows);
  const average = averageScore(ownRows.flatMap((row) => row.grades));
  const gradeRows = ownRows.flatMap((row) =>
    row.grades.map((grade) => ({
      id: grade.id,
      subject: row.subjectLabel,
      type: grade.type,
      score: formatScore(grade.score),
      comments: grade.comments || 'Sin comentario',
    })),
  );
  const isLoading = [subjectsQuery, periodsQuery, enrollmentsQuery, gradesQuery].some((query) => query.isLoading);
  const loadError = [subjectsQuery.error, periodsQuery.error, enrollmentsQuery.error, gradesQuery.error].filter(Boolean).join(' ');
  const reloadAcademic = () => {
    void Promise.all([
      subjectsQuery.reload(),
      periodsQuery.reload(),
      enrollmentsQuery.reload(),
      gradesQuery.reload(),
    ]);
  };

  return (
    <section className="page-panel">
      <header>
        <h2>Panel del estudiante</h2>
        <p>Tu matrícula, calificaciones y estado se leen del sistema académico.</p>
      </header>

      <nav className="section-nav" aria-label="Secciones del panel">
        <a href="#estado">Estado</a>
        <a href="#materias">Materias</a>
        <a href="#calificaciones">Calificaciones</a>
        <a href="#inscripcion">Inscripción</a>
      </nav>

      {isLoading ? <p className="muted-copy">Cargando información académica...</p> : null}
      {loadError ? (
        <div className="stack-form">
          <p className="error-message">{loadError}</p>
          <Button variant="secondary" onClick={reloadAcademic}>
            Reintentar
          </Button>
        </div>
      ) : null}

      {!isLoading && !loadError ? (
        <>
          <div className="stats-grid" id="estado">
            <article className="stat-card">
              <h3>Materias inscritas</h3>
              <strong>{ownRows.length}</strong>
            </article>
            <article className="stat-card">
              <h3>Promedio</h3>
              <strong>{formatScore(average)}</strong>
            </article>
            <article className="stat-card">
              <h3>Estado</h3>
              <strong>{status.label}</strong>
              <p>{status.detail}</p>
            </article>
          </div>

          <div className="content-grid">
            <section className="panel-card" id="materias" aria-labelledby="student-subjects-title">
              <h3 id="student-subjects-title">Materias</h3>
              <DataTable
                caption="Materias inscritas"
                rows={ownRows}
                getRowId={(row) => row.id}
                emptyMessage="No tienes materias inscritas."
                columns={[
                  { key: 'subject', header: 'Materia', render: (row) => row.subjectLabel },
                  { key: 'period', header: 'Período', render: (row) => row.periodLabel },
                  { key: 'credits', header: 'Créditos', render: (row) => row.credits },
                  {
                    key: 'status',
                    header: 'Estado',
                    render: (row) => <span className={`status-badge status-badge--${row.status}`}>{row.statusLabel}</span>,
                  },
                ]}
              />
            </section>

            <section className="panel-card" id="calificaciones" aria-labelledby="student-grades-title">
              <h3 id="student-grades-title">Calificaciones</h3>
              <DataTable
                caption="Calificaciones del estudiante"
                rows={gradeRows}
                getRowId={(row) => row.id}
                emptyMessage="Todavía no hay calificaciones."
                columns={[
                  { key: 'subject', header: 'Materia', render: (row) => row.subject },
                  { key: 'type', header: 'Tipo', render: (row) => row.type },
                  { key: 'score', header: 'Nota', render: (row) => row.score },
                  { key: 'comments', header: 'Comentario', render: (row) => row.comments },
                ]}
              />
            </section>
          </div>

          <section className="panel-card" id="inscripcion" aria-labelledby="student-enroll-title">
            <h3 id="student-enroll-title">Inscripción</h3>
            <p className="muted-copy">La inscripción queda activa. El servidor confirma si ya existe.</p>
            {user ? (
              <StudentEnrollmentForm
                userId={user.id}
                subjects={subjectsQuery.subjects}
                periods={periodsQuery.periods}
                enrollments={enrollmentsQuery.enrollments.filter((enrollment) => enrollment.user_id === user.id)}
                onCreated={enrollmentsQuery.reload}
              />
            ) : null}
          </section>
        </>
      ) : null}

      <div className="panel-card">
        <TaskBoard useRemoteSource heading="Tareas académicas" />
      </div>
    </section>
  );
};
