import { useApi } from '../../auth/hooks/useApi';
import { ApiMethod } from '../../../types/auth';
import { routes } from '../../../utils/constants';
import { CancelRequest, SubscribeRequest } from '../../../types/subscription';

export const useSubscriptionApi = () => {
  const { sendRequest, sendProtectedRequest } = useApi();

  const getPlans = async () => {
    const url = routes.subscriptions.plans;
    const response = await sendRequest(ApiMethod.GET, url);
    return response.data;
  };

  const getSubscription = async () => {
    const url = routes.subscriptions.me;
    const response = await sendProtectedRequest(ApiMethod.GET, url);
    return response.data;
  };

  const subscribeToPremium = async (data: SubscribeRequest) => {
    const url = routes.subscriptions.premium;
    const response = await sendProtectedRequest(ApiMethod.POST, url, data);
    return response.data;
  };

  const cancelSubscription = async (data: CancelRequest) => {
    const url = routes.subscriptions.cancel;
    const response = await sendProtectedRequest(ApiMethod.PATCH, url, data);
    return response.data;
  };

  const reactivateSubscription = async () => {
    const url = routes.subscriptions.reactivate;
    const response = await sendProtectedRequest(ApiMethod.POST, url);
    return response.data;
  };

  const verifyPayment = async (reference: string) => {
    const url = `${routes.subscriptions.paymentCallback}?reference=${reference}`;
    const response = await sendRequest(ApiMethod.GET, url);
    return response;
  };

  const retryPayment = async () => {
    const url = routes.subscriptions.paymentRetry;
    const response = await sendProtectedRequest(ApiMethod.POST, url);
    return response.data;
  };

  const getUpdatePaymentMethodLink = async () => {
    const url = routes.subscriptions.cardUpdate;
    const response = await sendProtectedRequest(ApiMethod.GET, url);
    return response.data;
  };

  const getPaymentHistory = async (params?: {
    page?: number;
    page_size?: number;
  }) => {
    let url = routes.subscriptions.paymentHistory;

    if (params) {
      const queryParams = new URLSearchParams();
      if (params.page) queryParams.append('page', params.page.toString());
      if (params.page_size)
        queryParams.append('page_size', params.page_size.toString());
      url += `?${queryParams.toString()}`;
    }

    const response = await sendProtectedRequest(ApiMethod.GET, url);
    return response.data;
  };

  return {
    getPlans,
    getSubscription,
    subscribeToPremium,
    cancelSubscription,
    reactivateSubscription,
    verifyPayment,
    retryPayment,
    getUpdatePaymentMethodLink,
    getPaymentHistory,
  };
};
