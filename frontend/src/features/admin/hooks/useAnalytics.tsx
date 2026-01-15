import { useMutation, useQuery } from '@tanstack/react-query';
import { useAnalyticsApi } from './useAnalyticsApi';
import { useNavigate } from 'react-router-dom';
import { handleQueryError } from '../../../utils/utils';
import {
  ArticlePerformanceResponse,
  DashboardMetricsResponse,
  TrackActivityRequest,
  TrackActivityResponse,
} from '../../../types/admin';

export function useTrackActivity() {
  const { trackActivity: trackActivityApi } = useAnalyticsApi();

  const {
    mutate: trackActivity,
    mutateAsync: trackActivityAsync,
    isPending,
    isError,
    error,
  } = useMutation<TrackActivityResponse, Error, TrackActivityRequest>({
    mutationFn: (data: TrackActivityRequest) => trackActivityApi(data),

    onError: (error) => {
      // Silent fail for analytics tracking - don't disrupt user experience
      handleQueryError(error, 'Analytics tracking failed');
    },
  });

  return { trackActivity, trackActivityAsync, isPending, isError, error };
}

export function useDashboardMetrics(period: 'weekly' | 'monthly') {
  const { getDashboardMetrics } = useAnalyticsApi();
  const navigate = useNavigate();

  const {
    isPending,
    isError,
    data: metrics,
    error,
    refetch,
  } = useQuery<DashboardMetricsResponse>({
    queryKey: ['dashboardMetrics', period],
    queryFn: () => {
      const handleUnauthenticated = () => {
        navigate('/login');
      };
      return getDashboardMetrics(handleUnauthenticated, period);
    },
    staleTime: 1000 * 60 * 5, // 5 minutes - data is cached on backend anyway
    retry: 1, // Only retry once for admin endpoints
  });

  return { isPending, isError, metrics, error, refetch };
}

export function useArticlePerformance(
  articleId: string,
  period: 'weekly' | 'monthly',
  enabled: boolean = true
) {
  const { getArticlePerformance } = useAnalyticsApi();
  const navigate = useNavigate();

  const {
    isPending,
    isError,
    data: performance,
    error,
    refetch,
  } = useQuery<ArticlePerformanceResponse>({
    queryKey: ['articlePerformance', articleId, period],
    queryFn: () => {
      const handleUnauthenticated = () => {
        navigate('/login');
      };
      return getArticlePerformance(handleUnauthenticated, articleId, period);
    },
    enabled: enabled && !!articleId,
    staleTime: 1000 * 60 * 5, // 5 minutes
  });

  return { isPending, isError, performance, error, refetch };
}
