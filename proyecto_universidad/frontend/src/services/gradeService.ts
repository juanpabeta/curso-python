import { api } from '@/api/client';
import { endpoints } from '@/api/endpoints';
import type { Grade, GradeInput } from '@/types';
import { parseGrade, parseGradeList } from '@/services/parsers';

export const fetchGrades = async (): Promise<Grade[]> => {
  const response = await api.get<unknown>(endpoints.grades);
  return parseGradeList(response.data);
};

export const createGrade = async (payload: GradeInput): Promise<Grade> => {
  const response = await api.post<unknown>(endpoints.grades, payload);
  return parseGrade(response.data);
};

export const updateGrade = async (id: number, payload: GradeInput): Promise<Grade> => {
  const response = await api.put<unknown>(endpoints.grade(id), payload);
  return parseGrade(response.data);
};

export const deleteGrade = async (id: number): Promise<void> => {
  await api.delete(endpoints.grade(id));
};
