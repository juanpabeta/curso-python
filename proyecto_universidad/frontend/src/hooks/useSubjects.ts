import { fetchSubjects } from '@/services/subjectService';
import { useFetch } from '@/hooks/useFetch';

export const useSubjects = () => {
  const query = useFetch(fetchSubjects);

  return {
    subjects: query.data ?? [],
    error: query.error,
    isLoading: query.isLoading,
    reload: query.reload,
  };
};
