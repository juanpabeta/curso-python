import { fetchUsers } from '@/services/userService';
import { useFetch } from '@/hooks/useFetch';

export const useUsers = () => {
  const query = useFetch(fetchUsers);

  return {
    users: query.data ?? [],
    error: query.error,
    isLoading: query.isLoading,
    reload: query.reload,
  };
};
