import { api } from '@/api/client';
import { endpoints } from '@/api/endpoints';
import type { Enrollment, EnrollmentInput } from '@/types';
import { parseEnrollment, parseEnrollmentList } from '@/services/parsers';

export const fetchEnrollments = async (): Promise<Enrollment[]> => {
  const response = await api.get<unknown>(endpoints.enrollments);
  return parseEnrollmentList(response.data);
};

export const createEnrollment = async (payload: EnrollmentInput): Promise<Enrollment> => {
  const response = await api.post<unknown>(endpoints.enrollments, payload);
  return parseEnrollment(response.data);
};

export const updateEnrollment = async (id: number, payload: EnrollmentInput): Promise<Enrollment> => {
  const response = await api.put<unknown>(endpoints.enrollment(id), payload);
  return parseEnrollment(response.data);
};

export const deleteEnrollment = async (id: number): Promise<void> => {
  await api.delete(endpoints.enrollment(id));
};
