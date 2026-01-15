import {
  ArticlePerformanceResponse,
  DashboardMetricsResponse,
  TrackActivityRequest,
  TrackActivityResponse,
} from '../../../types/admin';
import { ApiMethod } from '../../../types/auth';
import { routes } from '../../../utils/constants';
import { useApi } from '../../auth/hooks/useApi';

export const useAnalyticsApi = () => {
  const { sendRequest, sendAuthGuardedRequest } = useApi();

  const trackActivity = async (
    data: TrackActivityRequest
  ): Promise<TrackActivityResponse> => {
    const url = routes.analytics.track;
    const response = await sendRequest(ApiMethod.POST, url, data);
    return response.data;
  };

  const getDashboardMetrics = async (
    userIsNotAuthenticatedCallback: () => void,
    period: 'weekly' | 'monthly' = 'weekly'
  ): Promise<DashboardMetricsResponse> => {
    const url = routes.analytics.dashboard;
    const params = new URLSearchParams({ period });

    const response = await sendAuthGuardedRequest(
      userIsNotAuthenticatedCallback,
      ApiMethod.GET,
      `${url}?${params}`
    );
    return response.data;
  };

  const getArticlePerformance = async (
    userIsNotAuthenticatedCallback: () => void,
    articleId: string,
    period: 'weekly' | 'monthly' = 'weekly'
  ): Promise<ArticlePerformanceResponse> => {
    const url = routes.analytics.articlePerformance(articleId);
    const params = new URLSearchParams({ period });

    const response = await sendAuthGuardedRequest(
      userIsNotAuthenticatedCallback,
      ApiMethod.GET,
      `${url}?${params}`
    );
    return response.data;
  };

  return {
    trackActivity,
    getDashboardMetrics,
    getArticlePerformance,
  };
};
