import { useMutation, useQuery } from '@tanstack/react-query';
import { useGeneralApi } from './useGeneralApi';
import {
  ContactRequest,
  NewsletterSubscribeRequest,
  SiteDetail,
} from '../types/types';
import { handleQueryError } from '../utils/utils';

export function useSiteDetail() {
  const { getSiteDetail } = useGeneralApi();

  const {
    isPending,
    isError,
    data: siteDetail,
    error,
  } = useQuery<SiteDetail>({
    queryKey: ['siteDetail'],
    queryFn: () => getSiteDetail(),
    staleTime: Infinity, // Site detail rarely changes
  });

  return { isPending, isError, siteDetail, error };
}

export function useSubscribeNewsletter() {
  const { subscribeNewsletter: subscribeNewsletterApi } = useGeneralApi();

  const {
    mutate: subscribeNewsletter,
    mutateAsync: subscribeNewsletterAsync,
    isPending,
    isError,
    error,
    isSuccess,
  } = useMutation<any, Error, NewsletterSubscribeRequest>({
    mutationFn: (data: NewsletterSubscribeRequest) =>
      subscribeNewsletterApi(data),
    onError: (error) => {
      handleQueryError(error, 'Newsletter subscription');
    },
  });

  return {
    subscribeNewsletter,
    subscribeNewsletterAsync,
    isPending,
    isError,
    error,
    isSuccess,
  };
}

export function useUnsubscribeNewsletter() {
  const { unsubscribeNewsletter: unsubscribeNewsletterApi } = useGeneralApi();

  const {
    mutate: unsubscribeNewsletter,
    mutateAsync: unsubscribeNewsletterAsync,
    isPending,
    isError,
    error,
    isSuccess,
  } = useMutation<void, Error, string>({
    mutationFn: (token: string) => unsubscribeNewsletterApi(token),
    onError: (error) => {
      handleQueryError(error, 'Newsletter unsubscribe');
    },
  });

  return {
    unsubscribeNewsletter,
    unsubscribeNewsletterAsync,
    isPending,
    isError,
    error,
    isSuccess,
  };
}

export function useSendContactMessage() {
  const { sendContactMessage: sendContactMessageApi } = useGeneralApi();

  const {
    mutate: sendContactMessage,
    mutateAsync: sendContactMessageAsync,
    isPending,
    isError,
    error,
    isSuccess,
    reset,
  } = useMutation<void, Error, ContactRequest>({
    mutationFn: (data: ContactRequest) => sendContactMessageApi(data),
    onError: (error) => {
      handleQueryError(error, 'Contact message');
    },
  });

  return {
    sendContactMessage,
    sendContactMessageAsync,
    isPending,
    isError,
    error,
    isSuccess,
    reset,
  };
}
