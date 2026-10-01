import type { AcademicPeriod, Enrollment, Grade, RoleRecord, Subject, UserRecord } from '@/types';
import {
  asArray,
  asBoolean,
  asNumber,
  asOptionalString,
  asRecord,
  asString,
} from '@/utils/guards';

const parseRole = (value: unknown): RoleRecord => {
  const record = asRecord(value);
  return {
    id: asNumber(record, 'id'),
    name: asString(record, 'name'),
    description: asOptionalString(record, 'description'),
  };
};

export const parseSubject = (value: unknown): Subject => {
  const record = asRecord(value);
  return {
    id: asNumber(record, 'id'),
    code: asString(record, 'code'),
    name: asString(record, 'name'),
    credits: asNumber(record, 'credits'),
    description: asOptionalString(record, 'description'),
  };
};

export const parseSubjectList = (value: unknown): Subject[] => asArray(value).map(parseSubject);

export const parsePeriod = (value: unknown): AcademicPeriod => {
  const record = asRecord(value);
  return {
    id: asNumber(record, 'id'),
    code: asString(record, 'code'),
    name: asString(record, 'name'),
    start_date: asString(record, 'start_date'),
    end_date: asString(record, 'end_date'),
  };
};

export const parsePeriodList = (value: unknown): AcademicPeriod[] => asArray(value).map(parsePeriod);

export const parseEnrollment = (value: unknown): Enrollment => {
  const record = asRecord(value);
  return {
    id: asNumber(record, 'id'),
    user_id: asNumber(record, 'user_id'),
    subject_id: asNumber(record, 'subject_id'),
    period_id: asNumber(record, 'period_id'),
    status: asString(record, 'status'),
  };
};

export const parseEnrollmentList = (value: unknown): Enrollment[] => asArray(value).map(parseEnrollment);

export const parseGrade = (value: unknown): Grade => {
  const record = asRecord(value);
  return {
    id: asNumber(record, 'id'),
    enrollment_id: asNumber(record, 'enrollment_id'),
    type: asString(record, 'type'),
    score: asNumber(record, 'score'),
    comments: asOptionalString(record, 'comments'),
  };
};

export const parseGradeList = (value: unknown): Grade[] => asArray(value).map(parseGrade);

export const parseUser = (value: unknown): UserRecord => {
  const record = asRecord(value);
  return {
    id: asNumber(record, 'id'),
    email: asString(record, 'email'),
    full_name: asString(record, 'full_name'),
    is_active: asBoolean(record, 'is_active'),
    is_superuser: asBoolean(record, 'is_superuser'),
    roles: asArray(record.roles).map(parseRole),
  };
};

export const parseUserList = (value: unknown): UserRecord[] => asArray(value).map(parseUser);

export const parseRoleList = (value: unknown): RoleRecord[] => asArray(value).map(parseRole);
