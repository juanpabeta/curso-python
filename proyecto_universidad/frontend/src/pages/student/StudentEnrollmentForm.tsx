import { FormEvent, useState } from 'react';
import { Button } from '@/components/ui/Button';
import { SelectField } from '@/components/ui/SelectField';
import { createEnrollment } from '@/services/enrollmentService';
import type { AcademicPeriod, Enrollment, Subject } from '@/types';
import { toUserMessage } from '@/utils/errors';
import { hasFieldErrors, validateEnrollmentForm, type EnrollmentFormValues } from '@/utils/validators';

interface StudentEnrollmentFormProps {
  userId: number;
  subjects: Subject[];
  periods: AcademicPeriod[];
  enrollments: Enrollment[];
  onCreated: () => Promise<void>;
}

const EMPTY_FORM: EnrollmentFormValues = {
  userId: '',
  subjectId: '',
  periodId: '',
  status: 'active',
};

export const StudentEnrollmentForm = ({
  userId,
  subjects,
  periods,
  enrollments,
  onCreated,
}: StudentEnrollmentFormProps) => {
  const [form, setForm] = useState<EnrollmentFormValues>(EMPTY_FORM);
  const [errors, setErrors] = useState<Partial<Record<keyof EnrollmentFormValues, string>>>({});
  const [message, setMessage] = useState('');
  const [messageTone, setMessageTone] = useState<'error' | 'success'>('error');
  const [isSaving, setIsSaving] = useState(false);

  const subjectOptions = subjects.map((subject) => ({
    value: String(subject.id),
    label: `${subject.code} · ${subject.name}`,
  }));
  const periodOptions = periods.map((period) => ({
    value: String(period.id),
    label: `${period.code} · ${period.name}`,
  }));

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setMessage('');

    const nextValues = { ...form, userId: String(userId), status: 'active' };
    const nextErrors = validateEnrollmentForm(nextValues);
    setErrors(nextErrors);
    if (hasFieldErrors(nextErrors)) {
      return;
    }

    const duplicate = enrollments.some(
      (enrollment) =>
        enrollment.user_id === userId &&
        enrollment.subject_id === Number(nextValues.subjectId) &&
        enrollment.period_id === Number(nextValues.periodId),
    );
    if (duplicate) {
      setMessageTone('error');
      setMessage('Ya existe una inscripción tuya para esa materia y período.');
      return;
    }

    setIsSaving(true);
    try {
      await createEnrollment({
        user_id: userId,
        subject_id: Number(nextValues.subjectId),
        period_id: Number(nextValues.periodId),
        status: 'active',
      });
      setForm(EMPTY_FORM);
      setMessageTone('success');
      setMessage('Inscripción registrada.');
      await onCreated();
    } catch (caught) {
      setMessageTone('error');
      setMessage(toUserMessage(caught));
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <form className="stack-form" onSubmit={(event) => void handleSubmit(event)} noValidate aria-describedby={message ? 'student-enrollment-message' : undefined}>
      <SelectField
        id="student-subject"
        label="Materia"
        value={form.subjectId}
        onChange={(subjectId) => setForm((current) => ({ ...current, subjectId }))}
        options={subjectOptions}
        placeholder="Selecciona una materia"
        error={errors.subjectId}
        required
      />
      <SelectField
        id="student-period"
        label="Período"
        value={form.periodId}
        onChange={(periodId) => setForm((current) => ({ ...current, periodId }))}
        options={periodOptions}
        placeholder="Selecciona un período"
        error={errors.periodId}
        required
      />
      {message ? (
        <p id="student-enrollment-message" className={messageTone === 'error' ? 'error-message' : 'banner banner--success'}>
          {message}
        </p>
      ) : null}
      <Button type="submit" isLoading={isSaving} loadingLabel="Inscribiendo...">
        Inscribirme
      </Button>
    </form>
  );
};
