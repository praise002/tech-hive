import { useMutation, useQuery } from '@tanstack/react-query';
import toast from 'react-hot-toast';
import {
  register as registerApi,
  login as loginApi,
} from '../services/apiAuth';
import { useLocation, useNavigate } from 'react-router-dom';
import { LoginUserData } from '../../../types/auth';

export function useRegister() {
  const {
    mutate: register,
    isPending,
    isError,
    error,
  } = useMutation({
    mutationFn: registerApi,
    onSuccess: () => {},
    onError: (error) => {
      console.error('Registration error:', error);
    },
  });
  return { register, isPending, isError, error };
}

export function useLogin() {
  const navigate = useNavigate();

  const { mutate: login, isPending } = useMutation({
    mutationFn: (credentials: LoginUserData) => loginApi(credentials),
    onSuccess: async () => {
      // Let components that need user data fetch it themselves using useUser()
      navigate('/');
    },
    onError: (err) => {
      console.error('ERROR', err);
      toast.error(''); // TODO;
    },
  });

  return { login, isPending };
}

// TODO: FIX LATER
export function useGoogleCallback(fetchTokens: () => Promise<any>) {
  const navigate = useNavigate();
  const location = useLocation();

  const params = new URLSearchParams(location.search);
  const state = params.get('state');

  const { data, isLoading, isError } = useQuery({
    queryKey: ['googleCallback', state],
    queryFn: fetchTokens,
    enabled: !!state,
    staleTime: Infinity,
    // cacheTime: 0,
    refetchOnMount: false,
    // refetchOnWindowsFocus: false,
    retry: false, // default=3
  });

  if (data) {
    const { refresh, access } = data;
    localStorage.setItem('refreshToken', refresh);
    localStorage.setItem('accessToken', access);
    navigate('/');
  }

  if (isError) {
    navigate(''); // TODO: LATER
  }

  return { isLoading };
}
