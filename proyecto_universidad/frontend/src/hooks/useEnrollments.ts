import { fetchEnrollments } from '@/services/enrollmentService';
import { useFetch } from '@/hooks/useFetch';

export const useEnrollments = () => {
  const query = useFetch(fetchEnrollments);

  return {
    enrollments: query.data ?? [],
    error: query.error,
    isLoading: query.isLoading,
    reload: query.reload,
  };
};
