import { AxiosError } from 'axios';
import { describe, expect, it } from 'vitest';
import { buildEnrollmentRows, describeStudentStatus, formatScore } from '@/utils/academicView';
import { toUserMessage } from '@/utils/errors';
import { hasFieldErrors, validateGradeForm, validateSubjectForm } from '@/utils/validators';
import type { Enrollment, Grade, Subject } from '@/types';

const subject: Subject = { id: 1, code: 'ALG', name: 'Algoritmos', credits: 4, description: null };
const enrollment: Enrollment = { id: 10, user_id: 2, subject_id: 1, period_id: 3, status: 'active' };
const grade: Grade = { id: 7, enrollment_id: 10, type: 'Parcial', score: 9.5, comments: null };

describe('validación académica de formularios', () => {
  it('rechaza una materia sin código y con créditos fuera de rango', () => {
    const errors = validateSubjectForm({ code: 'A', name: 'Algoritmos', credits: '13', description: '' });

    expect(errors.code).toMatch(/2 y 20/);
    expect(errors.credits).toMatch(/1 y 12/);
    expect(hasFieldErrors(errors)).toBe(true);
  });

  it('acepta una calificación dentro del contrato del backend', () => {
    const errors = validateGradeForm({
      enrollmentId: '10',
      type: 'Parcial',
      score: '90',
      comments: '',
    });

    expect(hasFieldErrors(errors)).toBe(false);
  });
});

const httpError = (status: number, detail: string): AxiosError => {
  const error = new AxiosError('Request failed');
  error.response = {
    status,
    data: { detail },
    statusText: 'Error',
    headers: {},
    config: {} as AxiosError['config'],
  } as AxiosError['response'];
  return error;
};

describe('mensajes de error seguros', () => {
  it('oculta detalles internos de un error 500', () => {
    expect(toUserMessage(httpError(500, 'sqlalchemy.exc.IntegrityError password_hash'))).toBe(
      'El servicio no está disponible en este momento. Inténtalo de nuevo más tarde.',
    );
  });

  it('conserva un mensaje de dominio seguro', () => {
    expect(toUserMessage(httpError(409, 'La inscripción ya existe para este usuario, materia y período'))).toBe(
      'La inscripción ya existe para este usuario, materia y período',
    );
  });
});

describe('vista académica del estudiante', () => {
  it('arma la fila solo con la materia y la nota asociadas', () => {
    const rows = buildEnrollmentRows(
      [enrollment],
      [subject],
      [{ id: 3, code: '2026-1', name: 'Primer período', start_date: '2026-01-15', end_date: '2026-06-15' }],
      [{ id: 2, email: 'student@universidad.test', full_name: 'Ana Ruiz', is_active: true, is_superuser: false, roles: [] }],
      [grade],
    );

    expect(rows).toHaveLength(1);
    expect(rows[0]?.subjectLabel).toBe('ALG · Algoritmos');
    expect(rows[0]?.average).toBe(9.5);
    expect(formatScore(rows[0]?.average ?? null)).toMatch(/9,5|9.5/);
    expect(describeStudentStatus(rows).label).toBe('En curso');
  });

  it('describe la ausencia de matrícula', () => {
    expect(describeStudentStatus([]).label).toBe('Sin matrícula');
  });
});
