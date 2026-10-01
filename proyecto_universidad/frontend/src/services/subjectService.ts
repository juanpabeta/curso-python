import { api } from '@/api/client';
import { endpoints } from '@/api/endpoints';
import type { Subject, SubjectInput } from '@/types';
import { parseSubject, parseSubjectList } from '@/services/parsers';

export const fetchSubjects = async (): Promise<Subject[]> => {
  const response = await api.get<unknown>(endpoints.subjects);
  return parseSubjectList(response.data);
};

export const createSubject = async (payload: SubjectInput): Promise<Subject> => {
  const response = await api.post<unknown>(endpoints.subjects, payload);
  return parseSubject(response.data);
};

export const updateSubject = async (id: number, payload: SubjectInput): Promise<Subject> => {
  const response = await api.put<unknown>(endpoints.subject(id), payload);
  return parseSubject(response.data);
};

export const deleteSubject = async (id: number): Promise<void> => {
  await api.delete(endpoints.subject(id));
};
