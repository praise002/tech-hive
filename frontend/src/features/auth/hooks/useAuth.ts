import { useMutation, useQueryClient } from '@tanstack/react-query';

// import {
//   register as registerApi,
//   verifyRegistrationOtp as verifyRegisterOtpApi,
//   resendRegistrationOtp as resendRegistrationOtpApi,
//   login as loginApi,
// } from '../services/apiAuth';
// import { useLocation, useNavigate } from 'react-router-dom';
import { LoginUserData } from '../../../types/auth';
import { useAuthApi } from './useAuthApi';
import toast from 'react-hot-toast';
import { useNavigate } from 'react-router-dom';
import { setToken } from '../../../utils/utils';

export function useEmail() {
  const queryClient = useQueryClient();
  const getEmail = () => queryClient.getQueryData(['email']);

  return { getEmail };
}

export function useRegister() {
  const queryClient = useQueryClient();
  const { register: registerApi } = useAuthApi();

  const {
    mutate: register,
    isPending,
    isError,
    error,
  } = useMutation({
    mutationFn: registerApi,
    onSuccess: (data) => {
      queryClient.setQueryData(['email'], data.data.email);
    },

    onError: (error) => {
      console.error('Registration error:', error);
    },
  });
  return { register, isPending, isError, error };
}

export function useRegisterOtp() {
  const queryClient = useQueryClient();
  const { verifyRegistrationOtp: verifyRegisterOtpApi } = useAuthApi();

  const {
    mutate: verifyRegistrationOtp,
    isPending,
    isError,
    error,
  } = useMutation({
    mutationFn: verifyRegisterOtpApi,
    onSuccess: () => {
      queryClient.removeQueries({ queryKey: ['email'] });
    },
    onError: (error) => {
      console.error('OTP Verification error:', error);
    },
  });
  return { verifyRegistrationOtp, isPending, isError, error };
}

export function useRegisterResendOtp() {
  const { resendRegistrationOtp: resendRegistrationOtpApi } = useAuthApi();

  const {
    mutate: resendRegistrationOtp,
    isPending,
    isError,
    error,
  } = useMutation({
    mutationFn: resendRegistrationOtpApi,
    onSuccess: () => {},
    onError: (error) => {
      console.error('OTP Verification error:', error);
    },
  });
  return { resendRegistrationOtp, isPending, isError, error };
}

export function useLogin() {
  const { login: loginApi } = useAuthApi();

  const {
    mutate: login,
    isPending,
    isError,
    error,
  } = useMutation({
    mutationFn: (credentials: LoginUserData) => loginApi(credentials),
    onSuccess: async () => {},
    onError: (error) => {
      console.error('Login error:', error);
    },
  });

  return { login, isPending, isError, error };
}

export function useLogout() {
  const { logout: logoutApi } = useAuthApi();

  const queryClient = useQueryClient();

  const { mutate: logout, isPending } = useMutation({
    mutationFn: logoutApi,
    onSuccess: () => {
      // Clears all user's cached data
      queryClient.removeQueries();
    },
    onError: (error) => {
      console.error('Logout error:', error);
    },
  });

  return { logout, isPending };
}

export function useLogoutAll() {
  const { logoutAll: logoutAllApi } = useAuthApi();

  const queryClient = useQueryClient();

  const { mutate: logoutAll, isPending } = useMutation({
    mutationFn: logoutAllApi,
    onSuccess: () => {
      // Clears all user's cached data
      queryClient.removeQueries();
    },
    onError: (error) => {
      console.error('Logout all devices error:', error);
    },
  });

  return { logoutAll, isPending };
}

export function useChangePassword() {
  const { changePassword: changePasswordApi } = useAuthApi();

  const { mutate: changePassword, isPending } = useMutation({
    mutationFn: changePasswordApi,
    onSuccess: () => {},
    onError: (error) => {
      console.error('Change Password error:', error);
    },
  });

  return { changePassword, isPending };
}

export function useRequestPasswordReset() {
  const { requestPasswordReset: requestPasswordResetApi } = useAuthApi();

  const { mutate: requestPasswordReset, isPending } = useMutation({
    mutationFn: requestPasswordResetApi,
    onSuccess: () => {},
    onError: (error) => {
      console.error('Request Password Reset error:', error);
    },
  });

  return { requestPasswordReset, isPending };
}

export function useVerifyPasswordResetOtp() {
  const { verifyPasswordResetOtp: verifyPasswordResetOtpApi } = useAuthApi();

  const { mutate: verifyPasswordResetOtp, isPending } = useMutation({
    mutationFn: verifyPasswordResetOtpApi,
    onSuccess: () => {},
    onError: (error) => {
      console.error('Verify Password Reset Otp error:', error);
    },
  });

  return { verifyPasswordResetOtp, isPending };
}

export function useCompletePasswordReset() {
  const { completePasswordReset: completePasswordResetApi } = useAuthApi();

  const { mutate: completePasswordReset, isPending } = useMutation({
    mutationFn: completePasswordResetApi,
    onSuccess: () => {},
    onError: (error) => {
      console.error('Complete Password Reset error:', error);
    },
  });

  return { completePasswordReset, isPending };
}

export const useGoogleSignup = () => {
  const { fetchAuthRegisterUrl: fetchAuthRegisterUrlApi } = useAuthApi();

  const { mutate: fetchAuthRegisterUrl, isPending } = useMutation({
    mutationFn: fetchAuthRegisterUrlApi,
    onSuccess: (authorizationUrl) => {
      window.location.href = authorizationUrl;
    },
    onError: (error) => {
      console.error('Error fetching auth URL:', error);
      // TODO: MOVE TO MUTATE CALLBACK
      toast.error('Failed to start Google signup. Please try again.');
    },
  });

  return { fetchAuthRegisterUrl, isPending };
};

export function useGoogleCallback() {
  // TODO: MOVE NAVIGATE OPERATION TO MUTATE FN LATER
  const navigate = useNavigate();
  const { handleGoogleCallback: handleGoogleCallbackApi } = useAuthApi();

  const { mutate: processCallback, isPending } = useMutation({
    mutationFn: ({ access, refresh }: { access: string; refresh: string }) =>
      handleGoogleCallbackApi(access, refresh),
    onSuccess: (data) => {
      setToken(data);
      toast.success('Successfully signed in with Google!');
      navigate('/', { replace: true });
    },
    onError: (error) => {
      console.error('Google callback error:', error);
      toast.error('Authentication failed. Please try again.');
      navigate('/login', { replace: true });
    },
  });

  return { processCallback, isPending };
}
