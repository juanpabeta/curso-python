import { api } from '@/api/client';
import { endpoints } from '@/api/endpoints';
import type { AcademicPeriod, AcademicPeriodInput } from '@/types';
import { parsePeriod, parsePeriodList } from '@/services/parsers';

export const fetchPeriods = async (): Promise<AcademicPeriod[]> => {
  const response = await api.get<unknown>(endpoints.periods);
  return parsePeriodList(response.data);
};

export const createPeriod = async (payload: AcademicPeriodInput): Promise<AcademicPeriod> => {
  const response = await api.post<unknown>(endpoints.periods, payload);
  return parsePeriod(response.data);
};

export const updatePeriod = async (id: number, payload: AcademicPeriodInput): Promise<AcademicPeriod> => {
  const response = await api.put<unknown>(endpoints.period(id), payload);
  return parsePeriod(response.data);
};

export const deletePeriod = async (id: number): Promise<void> => {
  await api.delete(endpoints.period(id));
};
