import { ApiMethod } from '../../../types/auth';
import { routes } from '../../../utils/constants';
import { useApi } from '../../auth/hooks/useApi';
import { DashboardMetricsResponse } from '../../../types/analytics';

export const useAnalyticsApi = () => {
  const { sendAuthGuardedRequest } = useApi();

  const getDashboardMetrics = async (
    userIsNotAuthenticatedCallback: () => void,
    period: 'weekly' | 'monthly' = 'weekly'
  ) => {
    const url = `${routes.analytics.dashboard}?period=${period}`;
    const response = await sendAuthGuardedRequest(
      userIsNotAuthenticatedCallback,
      ApiMethod.GET,
      url
    );
    return response.data as DashboardMetricsResponse;
  };

  return {
    getDashboardMetrics,
  };
};
