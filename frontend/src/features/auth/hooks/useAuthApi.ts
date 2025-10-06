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
import { getToken, safeLocalStorage } from '../../../utils/utils';

const storage = safeLocalStorage();

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

    return response;
  };

  const logoutAll = async () => {
    const response = await sendRequest(ApiMethod.POST, routes.auth.logoutAll);

    return response;
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

    storage.setItem('email', email);

    return response;
  };

  const verifyPasswordResetOtp = async (otpData: VerifyOtpData) => {
    const response = await sendRequest(
      ApiMethod.POST,
      routes.auth.verifyPasswordResetOtp,
      otpData
    );

    storage.removeItem('email');

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

  const fetchAuthUrl = async (url: string) => {
    const response = await sendRequest(ApiMethod.GET, url);

    return response.data.authorization_url;
  };

  const fetchAuthRegisterUrl = async () => {
    return fetchAuthUrl(routes.auth.googleRegister);
  };

  const fetchAuthLoginUrl = async () => {
    return fetchAuthUrl(routes.auth.googleLogin);
  };

  const handleGoogleCallback = async (access: string, refresh: string) => {
    return { access, refresh };
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
    fetchAuthRegisterUrl,
    fetchAuthLoginUrl,
    handleGoogleCallback,
  };
};
