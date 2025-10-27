import { useMutation } from '@tanstack/react-query';
import { useGeneralApi } from './useGeneralApi';

export function useSubscribeNewsletter() {
  const { subscribeNewsletter: subscribeNewsletterApi } = useGeneralApi();

  const {
    mutate: subscribeNewsletter,
    isPending,
    isError,
    error,
  } = useMutation({
    mutationFn: subscribeNewsletterApi,
    onSuccess: () => {},

    onError: (error) => {
      console.error('Subscription error:', error);
    },
  });
  return { subscribeNewsletter, isPending, isError, error };
}
