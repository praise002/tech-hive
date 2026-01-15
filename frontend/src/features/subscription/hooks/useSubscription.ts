import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useEffect } from 'react';
import { useSubscriptionApi } from './useSubscriptionApi';
import {
  CancelRequest,
  SubscribeRequest,
  Subscription,
  SubscriptionPlan,
} from '../../../types/subscription';
import { handleQueryError } from '../../../utils/utils';
import toast from 'react-hot-toast';

export function usePlans() {
  const { getPlans } = useSubscriptionApi();

  const {
    data: plans,
    isPending,
    isError,
    error,
  } = useQuery<SubscriptionPlan[]>({
    queryKey: ['plans'],
    queryFn: getPlans,
    staleTime: Infinity, // Plans rarely change
  });

  return { plans, isPending, isError, error };
}

export function useMySubscription() {
  const { getSubscription } = useSubscriptionApi();

  const {
    data: subscription,
    isPending,
    isError,
    error,
  } = useQuery<Subscription>({
    queryKey: ['subscription'],
    queryFn: getSubscription,
    retry: false, // Don't retry 404s (no subscription)
  });

  return { subscription, isPending, isError, error };
}

export function useSubscribe() {
  const { subscribeToPremium } = useSubscriptionApi();
  const queryClient = useQueryClient();

  const {
    mutate: subscribe,
    isPending,
    isSuccess,
    isError,
    error,
    data,
  } = useMutation({
    mutationFn: (data: SubscribeRequest) => subscribeToPremium(data),
    onSuccess: (response) => {
      // If trial started, invalidate subscription
      if (response.status === 'TRIALING') {
        queryClient.invalidateQueries({ queryKey: ['subscription'] });
        toast.success('Trial started successfully!');
      }
      // If paid, the component will handle redirect to auth url
    },
    onError: (error) => {
      handleQueryError(error, 'Subscription failed');
    },
  });

  return { subscribe, isPending, isSuccess, isError, error, data };
}

export function useCancelSubscription() {
  const { cancelSubscription } = useSubscriptionApi();
  const queryClient = useQueryClient();

  const {
    mutate: cancel,
    isPending,
    isSuccess,
    isError,
    error,
  } = useMutation({
    mutationFn: (data: CancelRequest) => cancelSubscription(data),
    onSuccess: (response) => {
      queryClient.invalidateQueries({ queryKey: ['subscription'] });
      toast.success(
        `Subscription cancelled. Access until ${response.access_until}`
      );
    },
    onError: (error) => {
      handleQueryError(error, 'Cancellation failed');
    },
  });

  return { cancel, isPending, isSuccess, isError, error };
}

export function useReactivateSubscription() {
  const { reactivateSubscription } = useSubscriptionApi();
  const queryClient = useQueryClient();

  const {
    mutate: reactivate,
    isPending,
    isSuccess,
    isError,
    error,
  } = useMutation({
    mutationFn: reactivateSubscription,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['subscription'] });
      toast.success('Subscription reactivated successfully!');
    },
    onError: (error) => {
      handleQueryError(error, 'Reactivation failed');
    },
  });

  return { reactivate, isPending, isSuccess, isError, error };
}

export function useVerifyPayment(reference: string | null) {
  const { verifyPayment } = useSubscriptionApi();
  const queryClient = useQueryClient();

  const { data, isPending, isError, error, isSuccess } = useQuery({
    queryKey: ['verifyPayment', reference],
    queryFn: () => verifyPayment(reference!),
    enabled: !!reference,
    retry: false,
  });

  // Effect to invalidate subscription on success could be done in component or here if we used useMutation.
  // Since it's a query, we can rely on the user navigating away or component unmounting to re-trigger checks,
  // or we can manually invalidate in the component causing this hook to run.
  // Actually, standard pattern is to invalidate queries after effective mutation.
  // But this is a read-model sideEffect.
  useEffect(() => {
    if (isSuccess) {
      queryClient.invalidateQueries({ queryKey: ['subscription'] });
      queryClient.invalidateQueries({ queryKey: ['paymentHistory'] });
    }
  }, [isSuccess, queryClient]);

  return { data, isPending, isError, error, isSuccess };
}

export function useRetryPayment() {
  const { retryPayment } = useSubscriptionApi();
  const queryClient = useQueryClient();

  const {
    mutate: retry,
    isPending,
    isSuccess,
    isError,
    error,
  } = useMutation({
    mutationFn: retryPayment,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['subscription'] });
      queryClient.invalidateQueries({ queryKey: ['paymentHistory'] });
      toast.success('Payment retried successfully!');
    },
    onError: (error) => {
      handleQueryError(error, 'Payment retry failed');
    },
  });

  return { retry, isPending, isSuccess, isError, error };
}

export function usePaymentHistory(page: number = 1, pageSize: number = 10) {
  const { getPaymentHistory } = useSubscriptionApi();

  const {
    data: historyResponse,
    isPending,
    isError,
    error,
  } = useQuery({
    queryKey: ['paymentHistory', page, pageSize],
    queryFn: async () => {
      const response = await getPaymentHistory({ page, page_size: pageSize });
      return response;
    },
  });

  const history = historyResponse?.results || [];
  const count = historyResponse?.count;
  const next = historyResponse?.next;
  const previous = historyResponse?.previous;

  return { history, count, next, previous, isPending, isError, error };
}

export function useUpdatePaymentMethodLink() {
  const { getUpdatePaymentMethodLink } = useSubscriptionApi();

  const {
    refetch: getLink,
    isFetching,
    data,
    isError,
    error,
  } = useQuery({
    queryKey: ['updatePaymentMethodLink'],
    queryFn: getUpdatePaymentMethodLink,
    enabled: false, // Manual trigger only
  });

  return { getLink, isFetching, data, isError, error };
}
