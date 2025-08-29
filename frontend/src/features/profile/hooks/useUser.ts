import { useQuery } from '@tanstack/react-query';
import { getCurrentUser } from '../services/apiProfile';

export function useUser() {
  const {
    isPending,
    data: user,
    error,
  } = useQuery({
    queryKey: ['user'],
    queryFn: getCurrentUser,
  });

  const isAuthenticated = user && user.id;

  return { isPending, user, isAuthenticated, error };
}
