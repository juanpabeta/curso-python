import { FormEvent, useState } from 'react';
import { Alert } from '@/components/ui/Alert';
import { Button } from '@/components/ui/Button';
import { CheckboxField } from '@/components/ui/CheckboxField';
import { DataTable } from '@/components/ui/DataTable';
import { Modal } from '@/components/ui/Modal';
import { PageHeader } from '@/components/ui/PageHeader';
import { ResourceState } from '@/components/ui/ResourceState';
import { SelectField } from '@/components/ui/SelectField';
import { TextField } from '@/components/ui/TextField';
import { useAuth } from '@/hooks/useAuth';
import { useDocumentTitle } from '@/hooks/useDocumentTitle';
import { useRoles } from '@/hooks/useRoles';
import { useUsers } from '@/hooks/useUsers';
import { assignUserRole, createUser, deleteUser, updateUser } from '@/services/userService';
import type { UserRecord } from '@/types';
import { toUserMessage } from '@/utils/errors';
import { sanitizeText } from '@/utils/sanitize';
import {
  focusFirstInvalid,
  hasFieldErrors,
  validateUserForm,
  type UserFormValues,
} from '@/utils/validators';

const EMPTY_FORM: UserFormValues = {
  email: '',
  fullName: '',
  password: '',
  isActive: true,
  roleId: '',
};

const FIELD_IDS = {
  email: 'user-email',
  fullName: 'user-name',
  password: 'user-password',
  roleId: 'user-role',
};

export const UsersPage = () => {
  useDocumentTitle('Usuarios');
  const { user: sessionUser } = useAuth();
  const { users, error: usersError, isLoading: usersLoading, reload: reloadUsers } = useUsers();
  const { roles, error: rolesError, isLoading: rolesLoading, reload: reloadRoles } = useRoles();
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editing, setEditing] = useState<UserRecord | null>(null);
  const [pendingDelete, setPendingDelete] = useState<UserRecord | null>(null);
  const [form, setForm] = useState<UserFormValues>(EMPTY_FORM);
  const [fieldErrors, setFieldErrors] = useState<Partial<Record<string, string>>>({});
  const [notice, setNotice] = useState('');
  const [noticeTone, setNoticeTone] = useState<'success' | 'error'>('success');
  const [isSaving, setIsSaving] = useState(false);

  const roleOptions = roles.map((role) => ({ value: String(role.id), label: role.name }));

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

  const openEdit = (record: UserRecord) => {
    setEditing(record);
    setForm({
      email: record.email,
      fullName: record.full_name,
      password: '',
      isActive: record.is_active,
      roleId: '',
    });
    setFieldErrors({});
    setIsFormOpen(true);
  };

  const reload = async () => {
    await Promise.all([reloadUsers(), reloadRoles()]);
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const nextErrors = validateUserForm(form, editing ? 'edit' : 'create');
    setFieldErrors(nextErrors);
    if (hasFieldErrors(nextErrors)) {
      focusFirstInvalid(nextErrors, FIELD_IDS);
      return;
    }

    setIsSaving(true);
    try {
      if (editing) {
        await updateUser(editing.id, {
          email: sanitizeText(form.email).toLowerCase(),
          full_name: sanitizeText(form.fullName),
          is_active: form.isActive,
          ...(form.password ? { password: form.password } : {}),
        });
        if (form.roleId) {
          await assignUserRole(editing.id, Number(form.roleId));
        }
        setNotice('Usuario actualizado.');
      } else {
        const created = await createUser({
          email: sanitizeText(form.email).toLowerCase(),
          full_name: sanitizeText(form.fullName),
          password: form.password,
        });
        await assignUserRole(created.id, Number(form.roleId));
        setNotice('Usuario creado y rol asignado.');
      }
      setNoticeTone('success');
      closeForm();
      await reload();
    } catch (caught) {
      setNoticeTone('error');
      setNotice(toUserMessage(caught));
      await reload();
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
      await deleteUser(pendingDelete.id);
      setNoticeTone('success');
      setNotice('Usuario eliminado.');
      setPendingDelete(null);
      await reload();
    } catch (caught) {
      setNoticeTone('error');
      setNotice(toUserMessage(caught, 'No se pudo eliminar el usuario.'));
      setPendingDelete(null);
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <section className="page-panel">
      <PageHeader
        title="Usuarios"
        description="Crea cuentas, asigna roles y activa o desactiva el acceso."
        actions={<Button onClick={openCreate}>Nuevo usuario</Button>}
      />
      <Alert message={notice} tone={noticeTone} />
      <ResourceState isLoading={usersLoading || rolesLoading} error={usersError || rolesError} announce>
        <DataTable
          caption="Usuarios del sistema"
          rows={users}
          getRowId={(record) => record.id}
          emptyMessage="No hay usuarios para mostrar."
          columns={[
            { key: 'name', header: 'Nombre', render: (record) => record.full_name },
            { key: 'email', header: 'Correo', render: (record) => record.email },
            {
              key: 'roles',
              header: 'Roles',
              render: (record) => (record.roles.length > 0 ? record.roles.map((role) => role.name).join(', ') : 'Sin rol'),
            },
            { key: 'active', header: 'Estado', render: (record) => (record.is_active ? 'Activo' : 'Inactivo') },
            {
              key: 'actions',
              header: 'Acciones',
              render: (record) => (
                <div className="row-actions">
                  <Button variant="secondary" aria-label={`Editar ${record.full_name}`} onClick={() => openEdit(record)}>
                    Editar
                  </Button>
                  <Button
                    variant="danger"
                    aria-label={`Eliminar ${record.full_name}`}
                    disabled={record.id === sessionUser?.id}
                    onClick={() => setPendingDelete(record)}
                  >
                    Eliminar
                  </Button>
                </div>
              ),
            },
          ]}
        />
      </ResourceState>

      <Modal title={editing ? 'Editar usuario' : 'Nuevo usuario'} isOpen={isFormOpen} onClose={closeForm}>
        <form className="stack-form" onSubmit={(event) => void handleSubmit(event)} noValidate>
          <TextField
            id="user-email"
            label="Correo electrónico"
            type="email"
            value={form.email}
            onChange={(email) => setForm((current) => ({ ...current, email }))}
            error={fieldErrors.email}
            autoComplete="off"
            required
          />
          <TextField
            id="user-name"
            label="Nombre completo"
            value={form.fullName}
            onChange={(fullName) => setForm((current) => ({ ...current, fullName }))}
            error={fieldErrors.fullName}
            maxLength={200}
            autoComplete="name"
            required
          />
          <TextField
            id="user-password"
            label={editing ? 'Nueva contraseña' : 'Contraseña'}
            type="password"
            value={form.password}
            onChange={(password) => setForm((current) => ({ ...current, password }))}
            error={fieldErrors.password}
            hint={editing ? 'Déjala en blanco para conservar la actual.' : 'Mínimo 8 caracteres.'}
            autoComplete="new-password"
            required={!editing}
          />
          <SelectField
            id="user-role"
            label={editing ? 'Asignar rol adicional' : 'Rol'}
            value={form.roleId}
            onChange={(roleId) => setForm((current) => ({ ...current, roleId }))}
            options={roleOptions}
            placeholder="Selecciona un rol"
            error={fieldErrors.roleId}
            required={!editing}
          />
          {editing ? (
            <CheckboxField
              id="user-active"
              label="Usuario activo"
              checked={form.isActive}
              onChange={(isActive) => setForm((current) => ({ ...current, isActive }))}
            />
          ) : null}
          {editing && editing.roles.length > 0 ? (
            <p className="field-hint">Roles actuales: {editing.roles.map((role) => role.name).join(', ')}. La API no permite quitar un rol ya asignado.</p>
          ) : null}
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

      <Modal title="Eliminar usuario" isOpen={Boolean(pendingDelete)} onClose={() => setPendingDelete(null)}>
        <p>¿Eliminar a {pendingDelete?.full_name}? Esta acción no se puede deshacer.</p>
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
