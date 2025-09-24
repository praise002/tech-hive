import { ApiMethod } from '../../../types/auth';
import { API_URL } from '../../../utils/constants';
import { getToken } from '../../../utils/utils';

// Public APIs
const sendRequest = async (
  method: ApiMethod,
  path: string,
  body?: any,
  authToken?: string | null,
  init?: RequestInit
) => {
  const response = await fetch(API_URL + path, {
    method,
    ...(body && { body: JSON.stringify(body) }),
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...(authToken && { Authorization: `Bearer ${authToken}` }),
      ...init?.headers,
    },
  });

  if (!response.ok) {
    const error = await response.json();

    if (error.data) {
      throw error;
    } else {
      throw new Error(error.message || 'Request failed');
    }
  }

  return await response.json();
};

// Private APIs(login required)
const sendProtectedRequest = async (
  method: ApiMethod,
  path: string,
  body?: any,
  useRefreshToken = false, // Default to access token
  init?: RequestInit
) => {
  const authToken = useRefreshToken ? getToken()?.refresh : getToken()?.access;

  if (!authToken) throw new Error('No auth token found');

  return await sendRequest(method, path, body, authToken, init);
};

export const useApi = () => {
  return { sendRequest, sendProtectedRequest };
};
