export type RoleName = 'Administrador' | 'Docente' | 'Estudiante';

export interface UserSession {
  id: number;
  email: string;
  full_name: string;
  roles: RoleName[];
}

export interface Subject {
  id: number;
  code: string;
  name: string;
  credits: number;
  description?: string | null;
}

export interface AcademicPeriod {
  id: number;
  code: string;
  name: string;
  start_date: string;
  end_date: string;
}

export interface Enrollment {
  id: number;
  user_id: number;
  subject_id: number;
  period_id: number;
  status: string;
}

export interface Grade {
  id: number;
  enrollment_id: number;
  type: string;
  score: number;
  comments?: string | null;
}

export interface UserRecord {
  id: number;
  email: string;
  full_name: string;
  is_active: boolean;
  is_superuser: boolean;
  roles: Array<{ id: number; name: string; description?: string | null }>;
}

export interface ApiErrorPayload {
  detail?: string | ApiValidationIssue[];
  message?: string;
}

export interface ApiValidationIssue {
  loc?: Array<string | number>;
  msg?: string;
  type?: string;
}

export interface RoleRecord {
  id: number;
  name: string;
  description?: string | null;
}

export interface SubjectInput {
  code: string;
  name: string;
  credits: number;
  description?: string | null;
}

export interface AcademicPeriodInput {
  code: string;
  name: string;
  start_date: string;
  end_date: string;
}

export interface EnrollmentInput {
  user_id: number;
  subject_id: number;
  period_id: number;
  status: string;
}

export interface GradeInput {
  enrollment_id: number;
  type: string;
  score: number;
  comments?: string | null;
}

export interface UserInput {
  email: string;
  full_name: string;
  password: string;
}

export interface UserUpdateInput {
  email?: string;
  full_name?: string;
  password?: string;
  is_active?: boolean;
}

export const ENROLLMENT_STATUS_OPTIONS = [
  { value: 'active', label: 'Activa' },
  { value: 'completed', label: 'Completada' },
  { value: 'withdrawn', label: 'Retirada' },
] as const;

export const GRADE_TYPE_OPTIONS = ['Parcial', 'Final', 'Taller', 'Quiz', 'Proyecto'] as const;

export interface Task {
  id: string;
  title: string;
  completed: boolean;
}
