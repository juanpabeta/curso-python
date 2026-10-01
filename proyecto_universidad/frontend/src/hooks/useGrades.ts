import { fetchGrades } from '@/services/gradeService';
import { useFetch } from '@/hooks/useFetch';

export const useGrades = () => {
  const query = useFetch(fetchGrades);

  return {
    grades: query.data ?? [],
    error: query.error,
    isLoading: query.isLoading,
    reload: query.reload,
  };
};
