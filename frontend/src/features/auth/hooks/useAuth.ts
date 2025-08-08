import { useMutation, useQueryClient } from '@tanstack/react-query';
import toast from 'react-hot-toast';
import {
  register as registerApi,
  login as loginApi,
  getCurrentUser,
} from '../services/apiAuth';
import { useNavigate } from 'react-router-dom';
import { LoginUserData } from '../../../types/auth';

export function useRegister() {
  const { mutate: register, isPending } = useMutation({
    mutationFn: registerApi,
    onSuccess: (data) => {
      console.log(data); // TODO: REMOVE later
      // TODO: Navigate to page to input OTP
      toast.success(data?.message);
    },
    // TODO: ONERROR
  });
  return { register, isPending };
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
