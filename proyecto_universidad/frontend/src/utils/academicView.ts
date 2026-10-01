import type { AcademicPeriod, Enrollment, Grade, Subject, UserRecord } from '@/types';

export interface EnrollmentRow {
  id: number;
  userId: number;
  userLabel: string;
  subjectId: number;
  subjectLabel: string;
  credits: number;
  periodId: number;
  periodLabel: string;
  status: string;
  statusLabel: string;
  grades: Grade[];
  average: number | null;
}

const STATUS_LABELS: Record<string, string> = {
  active: 'Activa',
  completed: 'Completada',
  withdrawn: 'Retirada',
};

export const statusLabel = (status: string): string => STATUS_LABELS[status] ?? status;

export const averageScore = (grades: Grade[]): number | null => {
  if (grades.length === 0) {
    return null;
  }

  const total = grades.reduce((sum, grade) => sum + grade.score, 0);
  return total / grades.length;
};

export const formatScore = (value: number | null): string => {
  if (value === null || Number.isNaN(value)) {
    return 'Sin nota';
  }

  return value.toLocaleString('es-CO', { minimumFractionDigits: 1, maximumFractionDigits: 1 });
};

export const formatDate = (value: string): string => {
  const date = new Date(`${value}T00:00:00`);
  if (Number.isNaN(date.getTime())) {
    return value;
  }

  return date.toLocaleDateString('es-CO', { year: 'numeric', month: 'short', day: 'numeric' });
};

export const buildEnrollmentRows = (
  enrollments: Enrollment[],
  subjects: Subject[],
  periods: AcademicPeriod[],
  users: UserRecord[],
  grades: Grade[],
): EnrollmentRow[] => {
  const subjectById = new Map(subjects.map((subject) => [subject.id, subject]));
  const periodById = new Map(periods.map((period) => [period.id, period]));
  const userById = new Map(users.map((user) => [user.id, user]));

  return enrollments.map((enrollment) => {
    const subject = subjectById.get(enrollment.subject_id);
    const period = periodById.get(enrollment.period_id);
    const user = userById.get(enrollment.user_id);
    const relatedGrades = grades.filter((grade) => grade.enrollment_id === enrollment.id);

    return {
      id: enrollment.id,
      userId: enrollment.user_id,
      userLabel: user?.full_name ?? `Usuario ${enrollment.user_id}`,
      subjectId: enrollment.subject_id,
      subjectLabel: subject ? `${subject.code} · ${subject.name}` : `Materia ${enrollment.subject_id}`,
      credits: subject?.credits ?? 0,
      periodId: enrollment.period_id,
      periodLabel: period ? `${period.code} · ${period.name}` : `Período ${enrollment.period_id}`,
      status: enrollment.status,
      statusLabel: statusLabel(enrollment.status),
      grades: relatedGrades,
      average: averageScore(relatedGrades),
    };
  });
};

export interface AcademicStatusSummary {
  label: string;
  detail: string;
}

export const describeStudentStatus = (rows: EnrollmentRow[]): AcademicStatusSummary => {
  if (rows.length === 0) {
    return {
      label: 'Sin matrícula',
      detail: 'No hay inscripciones asociadas a tu usuario.',
    };
  }

  const activeRows = rows.filter((row) => row.status === 'active');
  const completedRows = rows.filter((row) => row.status === 'completed');
  const credits = activeRows.reduce((sum, row) => sum + row.credits, 0);

  if (activeRows.length > 0) {
    return {
      label: 'En curso',
      detail: `${activeRows.length} inscripción(es) activa(s) y ${credits} créditos en curso.`,
    };
  }

  if (completedRows.length === rows.length) {
    return {
      label: 'Completado',
      detail: 'Todas las inscripciones figuran como completadas.',
    };
  }

  return {
    label: 'Cerrado',
    detail: 'No hay inscripciones activas en este momento.',
  };
};
