import { useApi } from './useApi';
import {
  ApiMethod,
  ChangePasswordData,
  LoginUserData,
  PasswordResetCompleteData,
  RegisterUserData,
  VerifyOtpData,
} from '../../../types/auth';
import { routes } from '../../../utils/constants';
import { clearTokens, getToken, setToken } from '../../../utils/utils';

let debouncedPromise: Promise<unknown> | null;
let debouncedResolve: (...args: unknown[]) => void;
let debouncedReject: (...args: unknown[]) => void;
let timeout: ReturnType<typeof setTimeout>;

export const useAuthApi = () => {
  const { sendRequest, sendProtectedRequest } = useApi();

  const register = async (userData: RegisterUserData) => {
    const response = await sendRequest(
      ApiMethod.POST,
      routes.auth.register,
      userData
    );

    return response;
  };

  const verifyRegistrationOtp = async (otpData: VerifyOtpData) => {
    const response = await sendRequest(
      ApiMethod.POST,
      routes.auth.verifyRegOtp,
      otpData
    );

    return response;
  };

  const resendRegistrationOtp = async (email: string) => {
    const response = await sendRequest(
      ApiMethod.POST,
      routes.auth.resendRegOtp,
      { email }
    );

    return response;
  };

  const login = async (credentials: LoginUserData) => {
    const response = await sendRequest(
      ApiMethod.POST,
      routes.auth.login,
      credentials
    );
    setToken(response.data);
    return response;
  };

  const logout = async () => {
    const refresh = getToken().refresh;
    const response = await sendProtectedRequest(
      ApiMethod.POST,
      routes.auth.logout,
      {
        refresh,
      }
    );
    clearTokens();
    return response;
  };

  const logoutAll = async () => {
    const response = await sendRequest(ApiMethod.POST, routes.auth.logoutAll);
    clearTokens();
    return response;
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

  const changePassword = async (passwordData: ChangePasswordData) => {
    const response = await sendRequest(
      ApiMethod.POST,
      routes.auth.changePassword,
      passwordData
    );

    return response;
  };

  const requestPasswordReset = async (email: string) => {
    const response = await sendRequest(
      ApiMethod.POST,
      routes.auth.changePassword,
      { email }
    );

    return response;
  };

  const verifyPasswordResetOtp = async (otpData: VerifyOtpData) => {
    const response = await sendRequest(
      ApiMethod.POST,
      routes.auth.verifyPasswordResetOtp,
      otpData
    );

    return response;
  };

  const completePasswordReset = async (
    resetData: PasswordResetCompleteData
  ) => {
    const response = await sendRequest(
      ApiMethod.POST,
      routes.auth.completePasswordReset,
      resetData
    );

    return response;
  };

  const me = (userIsNotAuthenticatedCallback: () => void) => {
    return sendAuthGuardedRequest(
      userIsNotAuthenticatedCallback,
      ApiMethod.GET,
      routes.auth.me
    );
  };

  return {
    register,
    verifyRegistrationOtp,
    resendRegistrationOtp,
    login,
    logout,
    logoutAll,
    changePassword,
    requestPasswordReset,
    verifyPasswordResetOtp,
    completePasswordReset,
    me,
    sendAuthGuardedRequest,
  };
};
