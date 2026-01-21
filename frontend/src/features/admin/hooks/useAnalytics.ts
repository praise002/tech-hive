import { useQuery } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { useAnalyticsApi } from './useAnalyticsApi';
import { handleQueryError } from '../../../utils/utils';

export const useDashboardMetrics = (period: 'weekly' | 'monthly') => {
  const { getDashboardMetrics } = useAnalyticsApi();
  const navigate = useNavigate();

  const handleUnauthenticated = () => {
    navigate('/login');
  };

  const query = useQuery({
    queryKey: ['dashboardMetrics', period],
    queryFn: () => getDashboardMetrics(handleUnauthenticated, period),
    retry: 1,
  });

  if (query.isError) {
    handleQueryError(query.error, 'Dashboard metrics');
  }

  return query;
};
