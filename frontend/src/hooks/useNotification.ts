import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useNotificationApi } from './useNotificationApi';
import { handleQueryError } from '../utils/utils';

export function useNotifications(params?: Record<string, string>) {
  const { getNotifications } = useNotificationApi();

  const {
    data: notificationsResponse,
    isPending,
    isError,
    error,
  } = useQuery({
    queryKey: ['notifications', params],
    queryFn: async () => {
      const response = await getNotifications(params);
      return response;
    },
  });

  const notifications = notificationsResponse?.results || [];
  const count = notificationsResponse?.count;
  const next = notificationsResponse?.next;
  const previous = notificationsResponse?.previous;

  return { notifications, count, next, previous, isPending, isError, error };
}

export function useNotificationBadgeCount() {
  const { getNotificationBadgeCount } = useNotificationApi();

  const {
    data: badgeCount,
    isPending,
    isError,
    error,
  } = useQuery({
    queryKey: ['notificationBadge'],
    queryFn: () => getNotificationBadgeCount(),
    // Refetch often for live updates or use staleTime appropriately
    staleTime: 1000 * 60, // 1 minute
  });

  return { badgeCount, isPending, isError, error };
}

export function useNotification(id: string) {
  const { getNotification } = useNotificationApi();
  const queryClient = useQueryClient();

  const {
    data: notification,
    isPending,
    isError,
    error,
  } = useQuery({
    queryKey: ['notification', id],
    queryFn: async () => {
      const data = await getNotification(id);
      // Invalidate list/badge as reading a notification updates read status
      queryClient.invalidateQueries({ queryKey: ['notifications'] });
      queryClient.invalidateQueries({ queryKey: ['notificationBadge'] });
      return data;
    },
    enabled: !!id,
  });

  return { notification, isPending, isError, error };
}

export function useDeleteNotification() {
  const { deleteNotification: deleteNotificationApi } = useNotificationApi();
  const queryClient = useQueryClient();

  const {
    mutate: deleteNotification,
    isPending,
    isError,
    error,
    isSuccess,
  } = useMutation({
    mutationFn: (id: string) => deleteNotificationApi(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['notifications'] });
      queryClient.invalidateQueries({ queryKey: ['notificationBadge'] });
    },
    onError: (error) => {
      handleQueryError(error, 'Delete notification');
    },
  });

  return { deleteNotification, isPending, isError, error, isSuccess };
}

export function useRestoreNotification() {
  const { restoreNotification: restoreNotificationApi } = useNotificationApi();
  const queryClient = useQueryClient();

  const {
    mutate: restoreNotification,
    isPending,
    isError,
    error,
    isSuccess,
  } = useMutation({
    mutationFn: (id: string) => restoreNotificationApi(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['notifications'] });
      queryClient.invalidateQueries({ queryKey: ['notificationBadge'] });
    },
    onError: (error) => {
      handleQueryError(error, 'Restore notification');
    },
  });

  return { restoreNotification, isPending, isError, error, isSuccess };
}
