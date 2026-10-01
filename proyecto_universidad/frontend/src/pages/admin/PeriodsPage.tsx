import { FormEvent, useState } from 'react';
import { Alert } from '@/components/ui/Alert';
import { Button } from '@/components/ui/Button';
import { DataTable } from '@/components/ui/DataTable';
import { Modal } from '@/components/ui/Modal';
import { PageHeader } from '@/components/ui/PageHeader';
import { ResourceState } from '@/components/ui/ResourceState';
import { TextField } from '@/components/ui/TextField';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { usePeriods } from '@/hooks/usePeriods';
import { createPeriod, deletePeriod, updatePeriod } from '@/services/periodService';
import type { AcademicPeriod } from '@/types';
import { formatDate } from '@/utils/academicView';
import { toUserMessage } from '@/utils/errors';
import { sanitizeText } from '@/utils/sanitize';
import {
  focusFirstInvalid,
  hasFieldErrors,
  validatePeriodForm,
  type PeriodFormValues,
} from '@/utils/validators';

const EMPTY_FORM: PeriodFormValues = { code: '', name: '', startDate: '', endDate: '' };

const FIELD_IDS = {
  code: 'period-code',
  name: 'period-name',
  startDate: 'period-start',
  endDate: 'period-end',
};

export const PeriodsPage = () => {
  useDocumentTitle('Períodos');
  const { periods, error, isLoading, reload } = usePeriods();
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editing, setEditing] = useState<AcademicPeriod | null>(null);
  const [pendingDelete, setPendingDelete] = useState<AcademicPeriod | null>(null);
  const [form, setForm] = useState<PeriodFormValues>(EMPTY_FORM);
  const [fieldErrors, setFieldErrors] = useState<Partial<Record<keyof PeriodFormValues, string>>>({});
  const [notice, setNotice] = useState('');
  const [noticeTone, setNoticeTone] = useState<'success' | 'error'>('success');
  const [isSaving, setIsSaving] = useState(false);

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

  const openEdit = (period: AcademicPeriod) => {
    setEditing(period);
    setForm({
      code: period.code,
      name: period.name,
      startDate: period.start_date,
      endDate: period.end_date,
    });
    setFieldErrors({});
    setIsFormOpen(true);
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const nextErrors = validatePeriodForm(form);
    setFieldErrors(nextErrors);
    if (hasFieldErrors(nextErrors)) {
      focusFirstInvalid(nextErrors, FIELD_IDS);
      return;
    }

    const payload = {
      code: sanitizeText(form.code),
      name: sanitizeText(form.name),
      start_date: form.startDate,
      end_date: form.endDate,
    };

    setIsSaving(true);
    try {
      if (editing) {
        await updatePeriod(editing.id, payload);
        setNotice('Período actualizado.');
      } else {
        await createPeriod(payload);
        setNotice('Período creado.');
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
      await deletePeriod(pendingDelete.id);
      setNoticeTone('success');
      setNotice('Período eliminado.');
      setPendingDelete(null);
      await reload();
    } catch (caught) {
      setNoticeTone('error');
      setNotice(toUserMessage(caught, 'No se pudo eliminar el período. Puede tener inscripciones asociadas.'));
      setPendingDelete(null);
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <section className="page-panel">
      <PageHeader
        title="Períodos"
        description="Períodos académicos que habilitan las inscripciones."
        actions={<Button onClick={openCreate}>Nuevo período</Button>}
      />
      <Alert message={notice} tone={noticeTone} />
      <ResourceState isLoading={isLoading} error={error} announce>
        <DataTable
          caption="Períodos académicos"
          rows={periods}
          getRowId={(period) => period.id}
          emptyMessage="Todavía no hay períodos registrados."
          columns={[
            { key: 'code', header: 'Código', render: (period) => period.code },
            { key: 'name', header: 'Nombre', render: (period) => period.name },
            { key: 'start', header: 'Inicio', render: (period) => formatDate(period.start_date) },
            { key: 'end', header: 'Fin', render: (period) => formatDate(period.end_date) },
            {
              key: 'actions',
              header: 'Acciones',
              render: (period) => (
                <div className="row-actions">
                  <Button variant="secondary" aria-label={`Editar ${period.code}`} onClick={() => openEdit(period)}>
                    Editar
                  </Button>
                  <Button variant="danger" aria-label={`Eliminar ${period.code}`} onClick={() => setPendingDelete(period)}>
                    Eliminar
                  </Button>
                </div>
              ),
            },
          ]}
        />
      </ResourceState>

      <Modal title={editing ? 'Editar período' : 'Nuevo período'} isOpen={isFormOpen} onClose={closeForm}>
        <form className="stack-form" onSubmit={(event) => void handleSubmit(event)} noValidate>
          <TextField id="period-code" label="Código" value={form.code} onChange={(code) => setForm((current) => ({ ...current, code }))} error={fieldErrors.code} maxLength={20} required autoComplete="off" />
          <TextField id="period-name" label="Nombre" value={form.name} onChange={(name) => setForm((current) => ({ ...current, name }))} error={fieldErrors.name} maxLength={100} required autoComplete="off" />
          <TextField id="period-start" label="Fecha de inicio" type="date" value={form.startDate} onChange={(startDate) => setForm((current) => ({ ...current, startDate }))} error={fieldErrors.startDate} required />
          <TextField id="period-end" label="Fecha de fin" type="date" value={form.endDate} onChange={(endDate) => setForm((current) => ({ ...current, endDate }))} error={fieldErrors.endDate} required />
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

      <Modal title="Eliminar período" isOpen={Boolean(pendingDelete)} onClose={() => setPendingDelete(null)}>
        <p>¿Eliminar {pendingDelete?.name}? Esta acción no se puede deshacer.</p>
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
