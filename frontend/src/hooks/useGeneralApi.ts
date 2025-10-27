import { useApi } from '../features/auth/hooks/useApi';
import { ApiMethod } from '../types/auth';
import { routes } from '../utils/constants';

export const useGeneralApi = () => {
  const { sendRequest } = useApi();

  const subscribeNewsletter = async (email: string) => {
    const response = await sendRequest(
      ApiMethod.POST,
      routes.general.nesletter,
      email
    );

    return response;
  };

  const unsubscribeNewsletter = async (email: string) => {
    const response = await sendRequest(
      ApiMethod.DELETE,
      routes.general.nesletter,
      email
    );

    return response;
  };

  return {
    subscribeNewsletter,
    unsubscribeNewsletter,
  };
};
