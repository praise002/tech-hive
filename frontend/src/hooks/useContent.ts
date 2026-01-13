import { useQuery } from '@tanstack/react-query';
import { useContentApi } from './useContentApi';
import { useNavigate } from 'react-router-dom';

export function useCategories(params?: { page?: number; page_size?: number }) {
  const { getCategories } = useContentApi();

  const {
    isPending,
    isError,
    data: categoriesResponse,
    error,
  } = useQuery({
    queryKey: ['categories', params],
    queryFn: async () => {
      const response = await getCategories(params);
      return response;
    },
  });

  const categories = categoriesResponse?.results || [];
  const count = categoriesResponse?.count;
  const next = categoriesResponse?.next;
  const previous = categoriesResponse?.previous;

  return {
    isPending,
    isError,
    categories,
    count,
    next,
    previous,
    error,
  };
}

export function useArticles(params?: {
  limit?: number;
  page?: number;
  page_size?: number;
}) {
  const { getArticles } = useContentApi();

  const {
    isPending,
    isError,
    data: articlesResponse,
    error,
  } = useQuery({
    queryKey: ['articles', params],
    queryFn: async () => {
      const response = await getArticles(params);
      return response;
    },
  });

  const articles = articlesResponse?.results || [];
  const count = articlesResponse?.count;
  const next = articlesResponse?.next;
  const previous = articlesResponse?.previous;

  return {
    isPending,
    isError,
    articles,
    count,
    next,
    previous,
    error,
  };
}

export function useEvents(params?: { page?: number; page_size?: number }) {
  const { getEvents } = useContentApi();

  const {
    isPending,
    isError,
    data: eventsResponse,
    error,
  } = useQuery({
    queryKey: ['events', params],
    queryFn: async () => {
      const response = await getEvents(params);
      return response;
    },
  });

  const events = eventsResponse?.results || [];
  const count = eventsResponse?.count;
  const next = eventsResponse?.next;
  const previous = eventsResponse?.previous;

  return {
    isPending,
    isError,
    events,
    count,
    next,
    previous,
    error,
  };
}

export function useJobs(params?: { page?: number; page_size?: number }) {
  const { getJobs } = useContentApi();

  const {
    isPending,
    isError,
    data: jobsResponse,
    error,
  } = useQuery({
    queryKey: ['jobs', params],
    queryFn: async () => {
      const response = await getJobs(params);
      return response;
    },
  });

  const jobs = jobsResponse?.results || [];
  const count = jobsResponse?.count;
  const next = jobsResponse?.next;
  const previous = jobsResponse?.previous;

  return {
    isPending,
    isError,
    jobs,
    count,
    next,
    previous,
    error,
  };
}

export function useResources(params?: { page?: number; page_size?: number }) {
  const { getResources } = useContentApi();

  const {
    isPending,
    isError,
    data: resourcesResponse,
    error,
  } = useQuery({
    queryKey: ['resources', params],
    queryFn: async () => {
      const response = await getResources(params);
      return response;
    },
  });

  const resources = resourcesResponse?.results || [];
  const count = resourcesResponse?.count;
  const next = resourcesResponse?.next;
  const previous = resourcesResponse?.previous;

  return {
    isPending,
    isError,
    resources,
    count,
    next,
    previous,
    error,
  };
}

export function useTools(params?: { page?: number; page_size?: number }) {
  const { getTools } = useContentApi();

  const {
    isPending,
    isError,
    data: toolsResponse,
    error,
  } = useQuery({
    queryKey: ['tools', params],
    queryFn: async () => {
      const response = await getTools(params);
      return response;
    },
  });

  const tools = toolsResponse?.results || [];
  const count = toolsResponse?.count;
  const next = toolsResponse?.next;
  const previous = toolsResponse?.previous;

  return {
    isPending,
    isError,
    tools,
    count,
    next,
    previous,
    error,
  };
}

export function useArticleDetail(username: string, slug: string) {
  const { getArticleDetail } = useContentApi();

  const {
    isPending,
    isError,
    data: article,
    error,
  } = useQuery({
    queryKey: ['articleDetail', username, slug],
    queryFn: async () => {
      return getArticleDetail(username, slug);
    },
    enabled: !!slug && !!username,
  });

  return { isPending, isError, article, error };
}

export function useCategoryDetail(slug: string) {
  const { getCategoryDetail } = useContentApi();

  const {
    isPending,
    isError,
    data: category,
    error,
  } = useQuery({
    queryKey: ['categoryDetail', slug],
    queryFn: async () => {
      return getCategoryDetail(slug);
    },
    enabled: !!slug,
  });

  return { isPending, isError, category, error };
}

export function useJobDetail(jobId: string) {
  const { getJobDetail } = useContentApi();

  const {
    isPending,
    isError,
    data: job,
    error,
  } = useQuery({
    queryKey: ['jobDetail', jobId],
    queryFn: async () => {
      return getJobDetail(jobId);
    },
    enabled: !!jobId,
  });

  return { isPending, isError, job, error };
}

export function useEventDetail(eventId: string) {
  const { getEventDetail } = useContentApi();

  const {
    isPending,
    isError,
    data: event,
    error,
  } = useQuery({
    queryKey: ['eventDetail', eventId],
    queryFn: async () => {
      return getEventDetail(eventId);
    },
    enabled: !!eventId,
  });

  return { isPending, isError, event, error };
}

export function useResourceDetail(resourceId: string) {
  const { getResourceDetail } = useContentApi();

  const {
    isPending,
    isError,
    data: resource,
    error,
  } = useQuery({
    queryKey: ['resourceDetail', resourceId],
    queryFn: async () => {
      return getResourceDetail(resourceId);
    },
    enabled: !!resourceId,
  });

  return { isPending, isError, resource, error };
}

export function useToolDetail(toolId: string) {
  const { getToolDetail } = useContentApi();

  const {
    isPending,
    isError,
    data: tool,
    error,
  } = useQuery({
    queryKey: ['toolDetail', toolId],
    queryFn: async () => {
      return getToolDetail(toolId);
    },
    enabled: !!toolId,
  });

  return { isPending, isError, tool, error };
}
