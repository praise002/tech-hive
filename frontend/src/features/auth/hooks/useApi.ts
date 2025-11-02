import { ApiMethod } from '../../../types/auth';
import { API_URL, routes } from '../../../utils/constants';
import { getToken, setToken } from '../../../utils/utils';

let debouncedPromise: Promise<unknown> | null;
let debouncedResolve: (...args: unknown[]) => void;
let debouncedReject: (...args: unknown[]) => void;
let timeout: ReturnType<typeof setTimeout>;

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
    throw error;

    // if (error.data) {
    //   throw error;
    // } else {
    //   throw new Error(error.message || 'Request failed');
    // }
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

const refreshToken = async () => {
  clearTimeout(timeout);

  if (!debouncedPromise) {
    debouncedPromise = new Promise((resolve, reject) => {
      debouncedResolve = resolve;
      debouncedReject = reject;
    });
  }

  timeout = setTimeout(() => {
    const executeLogic = async () => {
      const response = await sendProtectedRequest(
        ApiMethod.POST,
        routes.auth.refreshTokens,
        {},
        true
      );
      setToken(response.data);
    };
    executeLogic().then(debouncedResolve).catch(debouncedReject);
    debouncedPromise = null;
  }, 200);

  return debouncedPromise;
};

const sendAuthGuardedRequest = async (
  userIsNotAuthenticatedCallback: () => void,
  method: ApiMethod,
  path: string,
  body?: any,
  init?: RequestInit
) => {
  try {
    return await sendProtectedRequest(method, path, body, undefined, init);
  } catch (e) {
    const error = e as { status?: number };
    if (error?.status === 401) {
      try {
        await refreshToken();
      } catch (e) {
        userIsNotAuthenticatedCallback();
        throw e;
      }
      return await sendProtectedRequest(method, path, body, undefined, init);
    }

    throw e;
  }
};

export const useApi = () => {
  return { sendRequest, sendProtectedRequest, sendAuthGuardedRequest };
};
