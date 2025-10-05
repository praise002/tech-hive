import { useSearchParams } from 'react-router-dom';
import { useGoogleCallback } from '../hooks/useAuth';
import { useEffect } from 'react';
import Spinner from '../../../components/common/Spinner';

export const GoogleCallback = () => {
  const [searchParams] = useSearchParams();
  const { processCallback } = useGoogleCallback();

  useEffect(() => {
    const access = searchParams.get('access');
    const refresh = searchParams.get('refresh');

    if (access && refresh) {
      processCallback({ access, refresh });
    }
  }, [searchParams, processCallback]);

  return (
    <div className="min-h-screen flex items-center justify-center">
      <Spinner />
    </div>
  );
};
