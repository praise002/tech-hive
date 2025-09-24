import { useMutation, useQueryClient } from '@tanstack/react-query';

import {
  register as registerApi,
  verifyRegistrationOtp as verifyRegisterOtpApi,
  resendRegistrationOtp as resendRegistrationOtpApi,
  login as loginApi,
} from '../services/apiAuth';
// import { useLocation, useNavigate } from 'react-router-dom';
import { LoginUserData } from '../../../types/auth';

export function useEmail() {
  const queryClient = useQueryClient();
  const getEmail = () => queryClient.getQueryData(['email']);

  return { getEmail };
}

export function useRegister() {
  const queryClient = useQueryClient();
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

// TODO: FIX LATER
// export function useGoogleCallback(fetchTokens: () => Promise<any>) {
//   const navigate = useNavigate();
//   const location = useLocation();

//   const params = new URLSearchParams(location.search);
//   const state = params.get('state');

//   const { data, isLoading, isError } = useQuery({
//     queryKey: ['googleCallback', state],
//     queryFn: fetchTokens,
//     enabled: !!state,
//     staleTime: Infinity,
//     // cacheTime: 0,
//     refetchOnMount: false,
//     // refetchOnWindowsFocus: false,
//     retry: false, // default=3
//   });

//   if (data) {
//     const { refresh, access } = data;
//     localStorage.setItem('refreshToken', refresh);
//     localStorage.setItem('accessToken', access);
//     navigate('/');
//   }

//   if (isError) {
//     navigate(''); // TODO: LATER
//   }

//   return { isLoading };
// }
