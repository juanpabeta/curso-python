import { FormEvent, useState } from 'react';
import { Alert } from '@/components/ui/Alert';
import { Button } from '@/components/ui/Button';
import { DataTable } from '@/components/ui/DataTable';
import { Modal } from '@/components/ui/Modal';
import { PageHeader } from '@/components/ui/PageHeader';
import { ResourceState } from '@/components/ui/ResourceState';
import { TextField } from '@/components/ui/TextField';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { useSubjects } from '@/hooks/useSubjects';
import { createSubject, deleteSubject, updateSubject } from '@/services/subjectService';
import type { Subject } from '@/types';
import { toUserMessage } from '@/utils/errors';
import { sanitizeText } from '@/utils/sanitize';
import {
  focusFirstInvalid,
  hasFieldErrors,
  validateSubjectForm,
  type SubjectFormValues,
} from '@/utils/validators';

const EMPTY_FORM: SubjectFormValues = { code: '', name: '', credits: '3', description: '' };

const FIELD_IDS = {
  code: 'subject-code',
  name: 'subject-name',
  credits: 'subject-credits',
  description: 'subject-description',
};

export const SubjectsPage = () => {
  useDocumentTitle('Materias');
  const { subjects, error, isLoading, reload } = useSubjects();
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editing, setEditing] = useState<Subject | null>(null);
  const [pendingDelete, setPendingDelete] = useState<Subject | null>(null);
  const [form, setForm] = useState<SubjectFormValues>(EMPTY_FORM);
  const [fieldErrors, setFieldErrors] = useState<Partial<Record<keyof SubjectFormValues, string>>>({});
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

  const openEdit = (subject: Subject) => {
    setEditing(subject);
    setForm({
      code: subject.code,
      name: subject.name,
      credits: String(subject.credits),
      description: subject.description ?? '',
    });
    setFieldErrors({});
    setIsFormOpen(true);
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const nextErrors = validateSubjectForm(form);
    setFieldErrors(nextErrors);
    if (hasFieldErrors(nextErrors)) {
      focusFirstInvalid(nextErrors, FIELD_IDS);
      return;
    }

    const payload = {
      code: sanitizeText(form.code),
      name: sanitizeText(form.name),
      credits: Number(form.credits),
      description: sanitizeText(form.description) || null,
    };

    setIsSaving(true);
    try {
      if (editing) {
        await updateSubject(editing.id, payload);
        setNotice('Materia actualizada.');
      } else {
        await createSubject(payload);
        setNotice('Materia creada.');
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
      await deleteSubject(pendingDelete.id);
      setNoticeTone('success');
      setNotice('Materia eliminada.');
      setPendingDelete(null);
      await reload();
    } catch (caught) {
      setNoticeTone('error');
      setNotice(toUserMessage(caught, 'No se pudo eliminar la materia. Puede estar en uso.'));
      setPendingDelete(null);
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <section className="page-panel">
      <PageHeader
        title="Materias"
        description="Alta, consulta, edición y baja del catálogo académico."
        actions={<Button onClick={openCreate}>Nueva materia</Button>}
      />
      <Alert message={notice} tone={noticeTone} />
      <ResourceState isLoading={isLoading} error={error} announce>
        <DataTable
          caption="Catálogo de materias"
          rows={subjects}
          getRowId={(subject) => subject.id}
          emptyMessage="Todavía no hay materias registradas."
          columns={[
            { key: 'code', header: 'Código', render: (subject) => subject.code },
            { key: 'name', header: 'Nombre', render: (subject) => subject.name },
            { key: 'credits', header: 'Créditos', render: (subject) => subject.credits },
            {
              key: 'description',
              header: 'Descripción',
              render: (subject) => subject.description || 'Sin descripción',
            },
            {
              key: 'actions',
              header: 'Acciones',
              render: (subject) => (
                <div className="row-actions">
                  <Button variant="secondary" aria-label={`Editar ${subject.code}`} onClick={() => openEdit(subject)}>
                    Editar
                  </Button>
                  <Button variant="danger" aria-label={`Eliminar ${subject.code}`} onClick={() => setPendingDelete(subject)}>
                    Eliminar
                  </Button>
                </div>
              ),
            },
          ]}
        />
      </ResourceState>

      <Modal title={editing ? 'Editar materia' : 'Nueva materia'} isOpen={isFormOpen} onClose={closeForm}>
        <form className="stack-form" onSubmit={(event) => void handleSubmit(event)} noValidate>
          <TextField id="subject-code" label="Código" value={form.code} onChange={(code) => setForm((current) => ({ ...current, code }))} error={fieldErrors.code} maxLength={20} required autoComplete="off" />
          <TextField id="subject-name" label="Nombre" value={form.name} onChange={(name) => setForm((current) => ({ ...current, name }))} error={fieldErrors.name} maxLength={200} required autoComplete="off" />
          <TextField id="subject-credits" label="Créditos" type="number" min={1} max={12} value={form.credits} onChange={(credits) => setForm((current) => ({ ...current, credits }))} error={fieldErrors.credits} hint="Entero entre 1 y 12." required />
          <TextField id="subject-description" label="Descripción" value={form.description} onChange={(description) => setForm((current) => ({ ...current, description }))} error={fieldErrors.description} maxLength={500} multiline />
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

      <Modal title="Eliminar materia" isOpen={Boolean(pendingDelete)} onClose={() => setPendingDelete(null)}>
        <p>¿Eliminar {pendingDelete?.code}? Esta acción no se puede deshacer.</p>
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
