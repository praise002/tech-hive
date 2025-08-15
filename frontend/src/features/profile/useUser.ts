import { useQuery } from '@tanstack/react-query';
import { getCurrentUser } from './apiProfile';

export function useUser() {
  const {
    isPending,
    data: user,
    error,
  } = useQuery({
    queryKey: ['user'],
    queryFn: getCurrentUser,
    retry: false, // TODO: Learn about it Don't retry on auth failures
  });

  const isAuthenticated = user && user.id;

  return { isPending, user, isAuthenticated, error };
}
