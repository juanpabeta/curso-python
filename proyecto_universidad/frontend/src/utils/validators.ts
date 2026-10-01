export const TASK_TITLE_MAX_LENGTH = 120;

export const isValidEmail = (value: string): boolean => {
  const email = value.trim();
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
};

export const validateTaskTitle = (value: string, maxLength = TASK_TITLE_MAX_LENGTH): string | undefined => {
  const title = value.trim();

  if (!title) {
    return 'Escribe el título de la tarea.';
  }

  if (title.length > maxLength) {
    return `El título no puede superar ${maxLength} caracteres.`;
  }

  return undefined;
};

export const validatePassword = (value: string): string | undefined => {
  if (value.length < 8) {
    return 'La contraseña debe tener al menos 8 caracteres.';
  }

  return undefined;
};

export const capitalize = (value: string): string => value.charAt(0).toUpperCase() + value.slice(1);

export interface SubjectFormValues {
  code: string;
  name: string;
  credits: string;
  description: string;
}

export interface UserFormValues {
  email: string;
  fullName: string;
  password: string;
  isActive: boolean;
  roleId: string;
}

export interface PeriodFormValues {
  code: string;
  name: string;
  startDate: string;
  endDate: string;
}

export interface EnrollmentFormValues {
  userId: string;
  subjectId: string;
  periodId: string;
  status: string;
}

export interface GradeFormValues {
  enrollmentId: string;
  type: string;
  score: string;
  comments: string;
}

export type FieldErrors<Key extends string> = Partial<Record<Key, string>>;

const within = (value: string, min: number, max: number): boolean => {
  const length = value.trim().length;
  return length >= min && length <= max;
};

export const validateSubjectForm = (values: SubjectFormValues): FieldErrors<keyof SubjectFormValues> => {
  const errors: FieldErrors<keyof SubjectFormValues> = {};
  const code = values.code.trim();
  const name = values.name.trim();
  const credits = Number(values.credits);

  if (!within(code, 2, 20)) {
    errors.code = 'El código debe tener entre 2 y 20 caracteres.';
  }

  if (!within(name, 2, 200)) {
    errors.name = 'El nombre debe tener entre 2 y 200 caracteres.';
  }

  if (!Number.isInteger(credits) || credits < 1 || credits > 12) {
    errors.credits = 'Los créditos deben ser un entero entre 1 y 12.';
  }

  if (values.description.trim().length > 500) {
    errors.description = 'La descripción no puede superar 500 caracteres.';
  }

  return errors;
};

export const validateUserForm = (
  values: UserFormValues,
  mode: 'create' | 'edit',
): FieldErrors<'email' | 'fullName' | 'password' | 'roleId'> => {
  const errors: FieldErrors<'email' | 'fullName' | 'password' | 'roleId'> = {};

  if (!isValidEmail(values.email)) {
    errors.email = 'Ingresa un correo válido, sin espacios.';
  }

  if (!within(values.fullName, 2, 200)) {
    errors.fullName = 'El nombre debe tener entre 2 y 200 caracteres.';
  }

  const password = values.password;
  if (mode === 'create' || password.length > 0) {
    if (password.length < 8 || password.length > 128) {
      errors.password = 'La contraseña debe tener entre 8 y 128 caracteres.';
    }
  }

  if (mode === 'create' && !values.roleId) {
    errors.roleId = 'Selecciona un rol para el usuario.';
  }

  return errors;
};

export const validatePeriodForm = (values: PeriodFormValues): FieldErrors<keyof PeriodFormValues> => {
  const errors: FieldErrors<keyof PeriodFormValues> = {};

  if (!within(values.code, 2, 20)) {
    errors.code = 'El código debe tener entre 2 y 20 caracteres.';
  }

  if (!within(values.name, 2, 100)) {
    errors.name = 'El nombre debe tener entre 2 y 100 caracteres.';
  }

  if (!values.startDate) {
    errors.startDate = 'Indica la fecha de inicio.';
  }

  if (!values.endDate) {
    errors.endDate = 'Indica la fecha de fin.';
  }

  if (values.startDate && values.endDate && values.endDate < values.startDate) {
    errors.endDate = 'La fecha de fin no puede ser anterior al inicio.';
  }

  return errors;
};

export const validateEnrollmentForm = (
  values: EnrollmentFormValues,
): FieldErrors<keyof EnrollmentFormValues> => {
  const errors: FieldErrors<keyof EnrollmentFormValues> = {};

  if (!values.userId) {
    errors.userId = 'Selecciona un estudiante.';
  }

  if (!values.subjectId) {
    errors.subjectId = 'Selecciona una materia.';
  }

  if (!values.periodId) {
    errors.periodId = 'Selecciona un período.';
  }

  if (!within(values.status, 2, 20)) {
    errors.status = 'Selecciona un estado válido.';
  }

  return errors;
};

export const validateGradeForm = (values: GradeFormValues): FieldErrors<keyof GradeFormValues> => {
  const errors: FieldErrors<keyof GradeFormValues> = {};
  const score = Number(values.score);

  if (!values.enrollmentId) {
    errors.enrollmentId = 'Selecciona una inscripción.';
  }

  if (!within(values.type, 2, 50)) {
    errors.type = 'El tipo debe tener entre 2 y 50 caracteres.';
  }

  if (values.score.trim() === '' || Number.isNaN(score) || score < 0 || score > 100) {
    errors.score = 'La nota debe estar entre 0 y 100.';
  }

  if (values.comments.trim().length > 500) {
    errors.comments = 'El comentario no puede superar 500 caracteres.';
  }

  return errors;
};

export const hasFieldErrors = (errors: object): boolean => Object.keys(errors).length > 0;

export const focusFirstInvalid = (errors: object, fieldIds: Record<string, string>): void => {
  const firstKey = Object.keys(errors)[0];
  if (!firstKey) {
    return;
  }

  const fieldId = fieldIds[firstKey];
  if (fieldId) {
    document.getElementById(fieldId)?.focus();
  }
};
