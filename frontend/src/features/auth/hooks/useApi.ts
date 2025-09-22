import { ApiMethod } from '../../../types/types';
import { API_URL } from '../../../utils/constants';
import { getToken } from '../../../utils/utils';

const sendRequest = (
  method: ApiMethod,
  path: string,
  body?: any,
  authToken?: string | null,
  init?: RequestInit
) => {
  return fetch(API_URL + path, {
    method,
    ...(body && { body: JSON.stringify(body) }),
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...(authToken && { Authorization: `Bearer ${authToken}` }),
      ...init?.headers,
    },
  }).then((response) => {
    if (response.status >= 400) {
      throw response;
    }
    return response.json();
  });
};

const sendProtectedRequest = (
  method: ApiMethod,
  path: string,
  body?: any,
  useRefreshToken = false, // Default to access token
  init?: RequestInit
) => {
  const authToken = useRefreshToken ? getToken()?.refresh : getToken()?.access;

  if (!authToken) throw new Error('No auth token found');

  return sendRequest(method, path, body, authToken, init);
};

export const useApi = () => {
  return { sendRequest, sendProtectedRequest };
};
