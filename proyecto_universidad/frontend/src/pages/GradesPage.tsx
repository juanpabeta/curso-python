import { FormEvent, useMemo, useState } from 'react';
import { Alert } from '@/components/ui/Alert';
import { Button } from '@/components/ui/Button';
import { DataTable } from '@/components/ui/DataTable';
import { Modal } from '@/components/ui/Modal';
import { PageHeader } from '@/components/ui/PageHeader';
import { ResourceState } from '@/components/ui/ResourceState';
import { SelectField } from '@/components/ui/SelectField';
import { TextField } from '@/components/ui/TextField';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { useEnrollments } from '@/hooks/useEnrollments';
import { useGrades } from '@/hooks/useGrades';
import { usePeriods } from '@/hooks/usePeriods';
import { useSubjects } from '@/hooks/useSubjects';
import { useUsers } from '@/hooks/useUsers';
import { createGrade, deleteGrade, updateGrade } from '@/services/gradeService';
import { GRADE_TYPE_OPTIONS, type Grade } from '@/types';
import { buildEnrollmentRows, formatScore } from '@/utils/academicView';
import { toUserMessage } from '@/utils/errors';
import { sanitizeText } from '@/utils/sanitize';
import {
  focusFirstInvalid,
  hasFieldErrors,
  validateGradeForm,
  type GradeFormValues,
} from '@/utils/validators';

interface GradesPageProps {
  allowDelete?: boolean;
  title?: string;
  description?: string;
}

interface GradeRow {
  id: number;
  enrollmentLabel: string;
  type: string;
  score: string;
  comments: string;
  grade: Grade;
}

const EMPTY_FORM: GradeFormValues = {
  enrollmentId: '',
  type: 'Parcial',
  score: '',
  comments: '',
};

const FIELD_IDS = {
  enrollmentId: 'grade-enrollment',
  type: 'grade-type',
  score: 'grade-score',
  comments: 'grade-comments',
};

export const GradesPage = ({
  allowDelete = false,
  title = 'Calificaciones',
  description = 'Registra y actualiza notas sobre inscripciones existentes.',
}: GradesPageProps) => {
  useDocumentTitle(title);
  const subjectsQuery = useSubjects();
  const periodsQuery = usePeriods();
  const usersQuery = useUsers();
  const enrollmentsQuery = useEnrollments();
  const gradesQuery = useGrades();
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editing, setEditing] = useState<Grade | null>(null);
  const [pendingDelete, setPendingDelete] = useState<Grade | null>(null);
  const [form, setForm] = useState<GradeFormValues>(EMPTY_FORM);
  const [fieldErrors, setFieldErrors] = useState<Partial<Record<keyof GradeFormValues, string>>>({});
  const [notice, setNotice] = useState('');
  const [noticeTone, setNoticeTone] = useState<'success' | 'error'>('success');
  const [isSaving, setIsSaving] = useState(false);

  const enrollmentRows = useMemo(
    () =>
      buildEnrollmentRows(
        enrollmentsQuery.enrollments,
        subjectsQuery.subjects,
        periodsQuery.periods,
        usersQuery.users,
        gradesQuery.grades,
      ),
    [enrollmentsQuery.enrollments, subjectsQuery.subjects, periodsQuery.periods, usersQuery.users, gradesQuery.grades],
  );

  const gradeRows = useMemo<GradeRow[]>(
    () =>
      gradesQuery.grades.map((grade) => {
        const enrollment = enrollmentRows.find((row) => row.id === grade.enrollment_id);
        return {
          id: grade.id,
          enrollmentLabel: enrollment ? `${enrollment.userLabel} · ${enrollment.subjectLabel}` : `Inscripción ${grade.enrollment_id}`,
          type: grade.type,
          score: formatScore(grade.score),
          comments: grade.comments || 'Sin comentario',
          grade,
        };
      }),
    [gradesQuery.grades, enrollmentRows],
  );

  const loadError = [subjectsQuery.error, periodsQuery.error, usersQuery.error, enrollmentsQuery.error, gradesQuery.error].find(Boolean) ?? '';
  const isLoading = [subjectsQuery, periodsQuery, usersQuery, enrollmentsQuery, gradesQuery].some((query) => query.isLoading);
  const enrollmentOptions = enrollmentRows.map((row) => ({
    value: String(row.id),
    label: `${row.userLabel} · ${row.subjectLabel} · ${row.periodLabel}`,
  }));
  const knownTypes = new Set<string>(GRADE_TYPE_OPTIONS);
  const typeOptions = knownTypes.has(form.type)
    ? GRADE_TYPE_OPTIONS.map((type) => ({ value: type, label: type }))
    : [{ value: form.type, label: form.type }, ...GRADE_TYPE_OPTIONS.map((type) => ({ value: type, label: type }))];

  const closeForm = () => {
    setIsFormOpen(false);
    setEditing(null);
    setFieldErrors({});
  };

  const openCreate = () => {
    setEditing(null);
    setForm(EMPTY_FORM);
    setFieldErrors({});
    setIsFormOpen(true);
  };

  const openEdit = (grade: Grade) => {
    setEditing(grade);
    setForm({
      enrollmentId: String(grade.enrollment_id),
      type: grade.type,
      score: String(grade.score),
      comments: grade.comments ?? '',
    });
    setFieldErrors({});
    setIsFormOpen(true);
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const nextErrors = validateGradeForm(form);
    setFieldErrors(nextErrors);
    if (hasFieldErrors(nextErrors)) {
      focusFirstInvalid(nextErrors, FIELD_IDS);
      return;
    }

    const payload = {
      enrollment_id: Number(form.enrollmentId),
      type: sanitizeText(form.type),
      score: Number(form.score),
      comments: sanitizeText(form.comments) || null,
    };

    setIsSaving(true);
    try {
      if (editing) {
        await updateGrade(editing.id, payload);
        setNotice('Calificación actualizada.');
      } else {
        await createGrade(payload);
        setNotice('Calificación registrada.');
      }
      setNoticeTone('success');
      closeForm();
      await gradesQuery.reload();
    } catch (caught) {
      setNoticeTone('error');
      setNotice(toUserMessage(caught));
    } finally {
      setIsSaving(false);
    }
  };

  const handleDelete = async () => {
    if (!pendingDelete) {
      return;
    }

    setIsSaving(true);
    try {
      await deleteGrade(pendingDelete.id);
      setNoticeTone('success');
      setNotice('Calificación eliminada.');
      setPendingDelete(null);
      await gradesQuery.reload();
    } catch (caught) {
      setNoticeTone('error');
      setNotice(toUserMessage(caught));
      setPendingDelete(null);
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <section className="page-panel">
      <PageHeader title={title} description={description} actions={<Button onClick={openCreate}>Nueva calificación</Button>} />
      <Alert message={notice} tone={noticeTone} />
      <ResourceState isLoading={isLoading} error={loadError} announce>
        <DataTable
          caption="Calificaciones registradas"
          rows={gradeRows}
          getRowId={(row) => row.id}
          emptyMessage="No hay calificaciones registradas."
          columns={[
            { key: 'enrollment', header: 'Inscripción', render: (row) => row.enrollmentLabel },
            { key: 'type', header: 'Tipo', render: (row) => row.type },
            { key: 'score', header: 'Nota', render: (row) => row.score },
            { key: 'comments', header: 'Comentario', render: (row) => row.comments },
            {
              key: 'actions',
              header: 'Acciones',
              render: (row) => (
                <div className="row-actions">
                  <Button variant="secondary" aria-label={`Editar calificación ${row.id}`} onClick={() => openEdit(row.grade)}>
                    Editar
                  </Button>
                  {allowDelete ? (
                    <Button variant="danger" aria-label={`Eliminar calificación ${row.id}`} onClick={() => setPendingDelete(row.grade)}>
                      Eliminar
                    </Button>
                  ) : null}
                </div>
              ),
            },
          ]}
        />
      </ResourceState>

      <Modal title={editing ? 'Editar calificación' : 'Nueva calificación'} isOpen={isFormOpen} onClose={closeForm}>
        <form className="stack-form" onSubmit={(event) => void handleSubmit(event)} noValidate>
          <SelectField id="grade-enrollment" label="Inscripción" value={form.enrollmentId} onChange={(enrollmentId) => setForm((current) => ({ ...current, enrollmentId }))} options={enrollmentOptions} error={fieldErrors.enrollmentId} required />
          <SelectField id="grade-type" label="Tipo" value={form.type} onChange={(type) => setForm((current) => ({ ...current, type }))} options={typeOptions} error={fieldErrors.type} required />
          <TextField id="grade-score" label="Nota" type="number" min={0} max={5} step="0.1" value={form.score} onChange={(score) => setForm((current) => ({ ...current, score }))} error={fieldErrors.score} hint="Valor entre 0 y 5." required />
          <TextField id="grade-comments" label="Comentario" value={form.comments} onChange={(comments) => setForm((current) => ({ ...current, comments }))} error={fieldErrors.comments} maxLength={500} multiline />
          <div className="inline-actions">
            <Button type="submit" isLoading={isSaving} loadingLabel="Guardando...">
              Guardar
            </Button>
            <Button variant="secondary" onClick={closeForm}>
              Cancelar
            </Button>
          </div>
        </form>
      </Modal>

      <Modal title="Eliminar calificación" isOpen={Boolean(pendingDelete)} onClose={() => setPendingDelete(null)}>
        <p>¿Eliminar la calificación {pendingDelete?.id}?</p>
        <div className="inline-actions">
          <Button variant="danger" isLoading={isSaving} loadingLabel="Eliminando..." onClick={() => void handleDelete()}>
            Eliminar
          </Button>
          <Button variant="secondary" onClick={() => setPendingDelete(null)}>
            Cancelar
          </Button>
        </div>
      </Modal>
    </section>
  );
};
