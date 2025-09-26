import { useApi } from './useApi';
import { ApiMethod } from '../../../types/auth';
import { routes } from '../../../utils/constants';

export const useProfileApi = () => {
  const { sendRequest, sendProtectedRequest, sendAuthGuardedRequest } =
    useApi();

  const me = (userIsNotAuthenticatedCallback: () => void) => {
    return sendAuthGuardedRequest(
      userIsNotAuthenticatedCallback,
      ApiMethod.GET,
      routes.auth.me
    );
  };

  return {
    me,
  };
};
