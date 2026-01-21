import { useApi } from '../features/auth/hooks/useApi';
import { ApiMethod } from '../types/auth';
import { routes } from '../utils/constants';

export const useNotificationApi = () => {
  const { sendAuthGuardedRequest } = useApi();

  const getNotifications = async (
    userIsNotAuthenticatedCallback: () => void,
    params?: Record<string, string>
  ) => {
    const url = routes.notifications.list;
    const queryParams = new URLSearchParams(params).toString();
    const finalUrl = queryParams ? `${url}?${queryParams}` : url;
    const response = await sendAuthGuardedRequest(
      userIsNotAuthenticatedCallback,
      ApiMethod.GET,
      finalUrl
    );
    return response.data;
  };

  const getNotificationBadgeCount = async (
    userIsNotAuthenticatedCallback: () => void
  ) => {
    const url = routes.notifications.badgeCount;
    const response = await sendAuthGuardedRequest(
      userIsNotAuthenticatedCallback,
      ApiMethod.GET,
      url
    );
    return response.data;
  };

  const getNotification = async (
    userIsNotAuthenticatedCallback: () => void,
    id: string
  ) => {
    const url = routes.notifications.detail(id);
    const response = await sendAuthGuardedRequest(
      userIsNotAuthenticatedCallback,
      ApiMethod.GET,
      url
    );
    return response.data;
  };

  const deleteNotification = async (
    userIsNotAuthenticatedCallback: () => void,
    id: string
  ) => {
    const url = routes.notifications.detail(id);
    const response = await sendAuthGuardedRequest(
      userIsNotAuthenticatedCallback,
      ApiMethod.DELETE,
      url
    );
    return response.data;
  };

  const restoreNotification = async (
    userIsNotAuthenticatedCallback: () => void,
    id: string
  ) => {
    const url = routes.notifications.restore(id);
    const response = await sendAuthGuardedRequest(
      userIsNotAuthenticatedCallback,
      ApiMethod.POST,
      url
    );
    return response.data;
  };

  return {
    getNotifications,
    getNotificationBadgeCount,
    getNotification,
    deleteNotification,
    restoreNotification,
  };
};
