import { useQuery } from '@tanstack/react-query';
import { getCurrentUserProfile } from './apiProfile';

export function useProfile() {
  const {
    isPending,
    isError,
    data: profile,
    error,
  } = useQuery({
    queryKey: ['profile'],
    queryFn: getCurrentUserProfile,
  });

  return { isPending, isError, profile, error };
}

// profiles/<str:username>/
