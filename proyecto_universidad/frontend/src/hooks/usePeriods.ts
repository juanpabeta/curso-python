import { fetchPeriods } from '@/services/periodService';
import { useFetch } from '@/hooks/useFetch';

export const usePeriods = () => {
  const query = useFetch(fetchPeriods);

  return {
    periods: query.data ?? [],
    error: query.error,
    isLoading: query.isLoading,
    reload: query.reload,
  };
};
