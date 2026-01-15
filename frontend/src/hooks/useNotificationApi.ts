import { useApi } from '../features/auth/hooks/useApi';
import { ApiMethod } from '../types/auth';
import { routes } from '../utils/constants';

export const useNotificationApi = () => {
  const { sendRequest } = useApi();

  const getNotifications = async (params?: Record<string, string>) => {
    const url = routes.notifications.list;
    const queryParams = new URLSearchParams(params).toString();
    const finalUrl = queryParams ? `${url}?${queryParams}` : url;
    const response = await sendRequest(ApiMethod.GET, finalUrl);
    return response.data;
  };

  const getNotificationBadgeCount = async () => {
    const url = routes.notifications.badgeCount;
    const response = await sendRequest(ApiMethod.GET, url);
    return response.data;
  };

  const getNotification = async (id: string) => {
    const url = routes.notifications.detail(id);
    const response = await sendRequest(ApiMethod.GET, url);
    return response.data;
  };

  const deleteNotification = async (id: string) => {
    const url = routes.notifications.detail(id);
    const response = await sendRequest(ApiMethod.DELETE, url);
    return response.data;
  };

  const restoreNotification = async (id: string) => {
    const url = routes.notifications.restore(id);
    const response = await sendRequest(ApiMethod.POST, url);
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
