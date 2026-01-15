import { useApi } from '../features/auth/hooks/useApi';
import { ApiMethod } from '../types/auth';
import { ContactRequest, NewsletterSubscribeRequest } from '../types/types';

import { routes } from '../utils/constants';

export const useGeneralApi = () => {
  const { sendRequest } = useApi();

  const getSiteDetail = async () => {
    const url = routes.general.siteDetail;
    const response = await sendRequest(ApiMethod.GET, url);
    return response.data;
  };

  const subscribeNewsletter = async (data: NewsletterSubscribeRequest) => {
    const url = routes.general.newsletter;
    const response = await sendRequest(ApiMethod.POST, url, data);
    return response;
  };

  const unsubscribeNewsletter = async (token: string) => {
    const url = `${routes.general.newsletter}unsubscribe/${token}/`;
    const response = await sendRequest(ApiMethod.GET, url);
    return response;
  };

  // SEND CONTACT MESSAGE (public)
  const sendContactMessage = async (data: ContactRequest) => {
    const url = routes.general.contact;
    const response = await sendRequest(ApiMethod.POST, url, data);
    return response;
  };

  return {
    getSiteDetail,
    subscribeNewsletter,
    unsubscribeNewsletter,
    sendContactMessage,
  };
};
