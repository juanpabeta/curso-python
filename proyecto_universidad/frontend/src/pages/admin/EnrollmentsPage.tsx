import { FormEvent, useMemo, useState } from 'react';
import { Alert } from '@/components/ui/Alert';
import { Button } from '@/components/ui/Button';
import { DataTable } from '@/components/ui/DataTable';
import { Modal } from '@/components/ui/Modal';
import { PageHeader } from '@/components/ui/PageHeader';
import { ResourceState } from '@/components/ui/ResourceState';
import { SelectField } from '@/components/ui/SelectField';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { useEnrollments } from '@/hooks/useEnrollments';
import { usePeriods } from '@/hooks/usePeriods';
import { useSubjects } from '@/hooks/useSubjects';
import { useUsers } from '@/hooks/useUsers';
import { createEnrollment, deleteEnrollment, updateEnrollment } from '@/services/enrollmentService';
import { ENROLLMENT_STATUS_OPTIONS, type Enrollment } from '@/types';
import { buildEnrollmentRows } from '@/utils/academicView';
import { toUserMessage } from '@/utils/errors';
import {
  focusFirstInvalid,
  hasFieldErrors,
  validateEnrollmentForm,
  type EnrollmentFormValues,
} from '@/utils/validators';

const EMPTY_FORM: EnrollmentFormValues = {
  userId: '',
  subjectId: '',
  periodId: '',
  status: 'active',
};

const FIELD_IDS = {
  userId: 'enrollment-user',
  subjectId: 'enrollment-subject',
  periodId: 'enrollment-period',
  status: 'enrollment-status',
};

export const EnrollmentsPage = () => {
  useDocumentTitle('Inscripciones');
  const subjectsQuery = useSubjects();
  const periodsQuery = usePeriods();
  const usersQuery = useUsers();
  const enrollmentsQuery = useEnrollments();
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editing, setEditing] = useState<Enrollment | null>(null);
  const [pendingDelete, setPendingDelete] = useState<Enrollment | null>(null);
  const [form, setForm] = useState<EnrollmentFormValues>(EMPTY_FORM);
  const [fieldErrors, setFieldErrors] = useState<Partial<Record<keyof EnrollmentFormValues, string>>>({});
  const [notice, setNotice] = useState('');
  const [noticeTone, setNoticeTone] = useState<'success' | 'error'>('success');
  const [isSaving, setIsSaving] = useState(false);

  const rows = useMemo(
    () =>
      buildEnrollmentRows(
        enrollmentsQuery.enrollments,
        subjectsQuery.subjects,
        periodsQuery.periods,
        usersQuery.users,
        [],
      ),
    [enrollmentsQuery.enrollments, subjectsQuery.subjects, periodsQuery.periods, usersQuery.users],
  );

  const loadError = subjectsQuery.error || periodsQuery.error || usersQuery.error || enrollmentsQuery.error;
  const isLoading = subjectsQuery.isLoading || periodsQuery.isLoading || usersQuery.isLoading || enrollmentsQuery.isLoading;

  const statusOptions = ENROLLMENT_STATUS_OPTIONS.some((option) => option.value === form.status)
    ? [...ENROLLMENT_STATUS_OPTIONS]
    : [...ENROLLMENT_STATUS_OPTIONS, { value: form.status, label: form.status }];
  const userOptions = usersQuery.users.map((user) => ({
    value: String(user.id),
    label: `${user.full_name} · ${user.email}`,
  }));
  const subjectOptions = subjectsQuery.subjects.map((subject) => ({ value: String(subject.id), label: `${subject.code} · ${subject.name}` }));
  const periodOptions = periodsQuery.periods.map((period) => ({ value: String(period.id), label: `${period.code} · ${period.name}` }));

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

  const openEdit = (enrollment: Enrollment) => {
    setEditing(enrollment);
    setForm({
      userId: String(enrollment.user_id),
      subjectId: String(enrollment.subject_id),
      periodId: String(enrollment.period_id),
      status: enrollment.status,
    });
    setFieldErrors({});
    setIsFormOpen(true);
  };

  const reload = async () => {
    await enrollmentsQuery.reload();
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const nextErrors = validateEnrollmentForm(form);
    setFieldErrors(nextErrors);
    if (hasFieldErrors(nextErrors)) {
      focusFirstInvalid(nextErrors, FIELD_IDS);
      return;
    }

    const payload = {
      user_id: Number(form.userId),
      subject_id: Number(form.subjectId),
      period_id: Number(form.periodId),
      status: form.status,
    };

    setIsSaving(true);
    try {
      if (editing) {
        await updateEnrollment(editing.id, payload);
        setNotice('Inscripción actualizada.');
      } else {
        await createEnrollment(payload);
        setNotice('Inscripción creada.');
      }
      setNoticeTone('success');
      closeForm();
      await reload();
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
      await deleteEnrollment(pendingDelete.id);
      setNoticeTone('success');
      setNotice('Inscripción eliminada.');
      setPendingDelete(null);
      await reload();
    } catch (caught) {
      setNoticeTone('error');
      setNotice(toUserMessage(caught, 'No se pudo eliminar la inscripción.'));
      setPendingDelete(null);
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <section className="page-panel">
      <PageHeader
        title="Inscripciones"
        description="Relaciona estudiantes, materias y períodos."
        actions={<Button onClick={openCreate}>Nueva inscripción</Button>}
      />
      <Alert message={notice} tone={noticeTone} />
      <ResourceState isLoading={isLoading} error={loadError} announce>
        <DataTable
          caption="Inscripciones académicas"
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
            {
              key: 'actions',
              header: 'Acciones',
              render: (row) => {
                const enrollment = enrollmentsQuery.enrollments.find((item) => item.id === row.id);
                if (!enrollment) {
                  return null;
                }
                return (
                  <div className="row-actions">
                    <Button variant="secondary" aria-label={`Editar inscripción ${row.id}`} onClick={() => openEdit(enrollment)}>
                      Editar
                    </Button>
                    <Button variant="danger" aria-label={`Eliminar inscripción ${row.id}`} onClick={() => setPendingDelete(enrollment)}>
                      Eliminar
                    </Button>
                  </div>
                );
              },
            },
          ]}
        />
      </ResourceState>

      <Modal title={editing ? 'Editar inscripción' : 'Nueva inscripción'} isOpen={isFormOpen} onClose={closeForm}>
        <form className="stack-form" onSubmit={(event) => void handleSubmit(event)} noValidate>
          <SelectField id="enrollment-user" label="Estudiante" value={form.userId} onChange={(userId) => setForm((current) => ({ ...current, userId }))} options={userOptions} error={fieldErrors.userId} required />
          <SelectField id="enrollment-subject" label="Materia" value={form.subjectId} onChange={(subjectId) => setForm((current) => ({ ...current, subjectId }))} options={subjectOptions} error={fieldErrors.subjectId} required />
          <SelectField id="enrollment-period" label="Período" value={form.periodId} onChange={(periodId) => setForm((current) => ({ ...current, periodId }))} options={periodOptions} error={fieldErrors.periodId} required />
          <SelectField id="enrollment-status" label="Estado" value={form.status} onChange={(status) => setForm((current) => ({ ...current, status }))} options={statusOptions} placeholder="Selecciona un estado" error={fieldErrors.status} required />
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

      <Modal title="Eliminar inscripción" isOpen={Boolean(pendingDelete)} onClose={() => setPendingDelete(null)}>
        <p>¿Eliminar la inscripción {pendingDelete?.id}? Las calificaciones asociadas pueden impedir la baja.</p>
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
