import { useMutation } from '@tanstack/react-query';
import { useGeneralApi } from './useGeneralApi';
import { handleQueryError } from '../utils/utils';

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
      handleQueryError(error, 'Newsletter Subscription');
    },
  });
  return { subscribeNewsletter, isPending, isError, error };
}
