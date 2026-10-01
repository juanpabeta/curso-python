import { fetchRoles } from '@/services/userService';
import { useFetch } from '@/hooks/useFetch';

export const useRoles = () => {
  const query = useFetch(fetchRoles);

  return {
    roles: query.data ?? [],
    error: query.error,
    isLoading: query.isLoading,
    reload: query.reload,
  };
};
