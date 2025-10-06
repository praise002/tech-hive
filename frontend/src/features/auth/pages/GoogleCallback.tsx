import { useNavigate, useSearchParams } from 'react-router-dom';
import { useGoogleCallback } from '../hooks/useAuth';
import { useEffect } from 'react';
import Spinner from '../../../components/common/Spinner';
import toast from 'react-hot-toast';

export const GoogleRegisterCallback = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { processCallback } = useGoogleCallback();

  useEffect(() => {
    const access = searchParams.get('access');
    const refresh = searchParams.get('refresh');

    if (access && refresh) {
      processCallback(
        { access, refresh },
        {
          onSuccess: () => {
            navigate('/', { replace: true });
          },
          onError: () => {
            toast.error('Authentication failed. Please try again.');
            navigate('/register', { replace: true });
          },
        }
      );
    }
  }, [searchParams, processCallback, navigate]);

  return (
    <div className="min-h-screen flex items-center justify-center">
      <Spinner />
    </div>
  );
};

export const GoogleLoginCallback = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { processCallback } = useGoogleCallback();

  useEffect(() => {
    const access = searchParams.get('access');
    const refresh = searchParams.get('refresh');

    if (access && refresh) {
      processCallback(
        { access, refresh },
        {
          onSuccess: () => {
            navigate('/', { replace: true });
          },
          onError: () => {
            toast.error('Authentication failed. Please try again.');
            navigate('/login', { replace: true });
          },
        }
      );
    }
  }, [searchParams, processCallback, navigate]);

  return (
    <div className="min-h-screen flex items-center justify-center">
      <Spinner />
    </div>
  );
};
