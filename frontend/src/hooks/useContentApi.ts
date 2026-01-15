import { useApi } from '../features/auth/hooks/useApi';
import { ApiMethod } from '../types/auth';
import { routes } from '../utils/constants';

export const useContentApi = () => {
  const { sendRequest, sendAuthGuardedRequest } = useApi();

  const getCategories = async (params?: {
    page?: number;
    page_size?: number;
    ordering?: number;
    search?: number;
  }) => {
    let url = routes.content.categories;

    if (params) {
      const searchParams = new URLSearchParams();

      if (params.page) {
        searchParams.append('page', params.page.toString());
      }

      if (params.page_size) {
        searchParams.append('page_size', params.page_size.toString());
      }

      if (params.search) {
        searchParams.append('search', params.search.toString());
      }

      if (params.ordering) {
        searchParams.append('search', params.ordering.toString());
      }

      // Only add '?' if we have params
      if (searchParams.toString()) {
        url = `${url}?${searchParams.toString()}`;
      }
    }
    const response = await sendRequest(ApiMethod.GET, url);

    return response.data;
  };

  const getEvents = async (params?: {
    page?: number;
    page_size?: number;
    category?: string;
    search?: string;
    start_date?: string;
    end_date?: string;
    start_date__gte?: string;
    start_date__lte?: string;
    end_date__gte?: string;
    end_date__lte?: string;
  }) => {
    let url = routes.content.events;

    if (params) {
      const searchParams = new URLSearchParams();

      if (params.page) {
        searchParams.append('page', params.page.toString());
      }

      if (params.page_size) {
        searchParams.append('page_size', params.page_size.toString());
      }

      if (params.category) {
        searchParams.append('category', params.category);
      }

      if (params.search) {
        searchParams.append('search', params.search.toString());
      }

      if (params.start_date__gte) {
        searchParams.append('start_date__gte', params.start_date__gte);
      }

      if (params.start_date__lte) {
        searchParams.append('start_date__lte', params.start_date__lte);
      }

      if (params.end_date__gte) {
        searchParams.append('end_date__gte', params.end_date__gte);
      }

      if (params.end_date__lte) {
        searchParams.append('end_date__lte', params.end_date__lte);
      }

      // Only add '?' if we have params
      if (searchParams.toString()) {
        url = `${url}?${searchParams.toString()}`;
      }
    }
    const response = await sendRequest(ApiMethod.GET, url);

    return response.data;
  };

  const getJobs = async (params?: {
    page?: number;
    page_size?: number;
    search?: string;
    category?: string;
    company__iexact?: string;
    location__iexact?: string;
    job_type?: string;
    work_mode?: string;
    salary__gte?: number;
    salary__lte?: number;
  }) => {
    let url = routes.content.jobs;

    if (params) {
      const searchParams = new URLSearchParams();

      if (params.page) {
        searchParams.append('page', params.page.toString());
      }

      if (params.page_size) {
        searchParams.append('page_size', params.page_size.toString());
      }

      if (params.search) {
        searchParams.append('search', params.search);
      }

      if (params.category) {
        searchParams.append('category', params.category);
      }

      if (params.company__iexact) {
        searchParams.append('company__iexact', params.company__iexact);
      }

      if (params.location__iexact) {
        searchParams.append('location__iexact', params.location__iexact);
      }

      if (params.job_type) {
        searchParams.append('job_type', params.job_type);
      }

      if (params.work_mode) {
        searchParams.append('work_mode', params.work_mode);
      }

      if (params.salary__gte !== undefined) {
        searchParams.append('salary__gte', params.salary__gte.toString());
      }

      if (params.salary__lte !== undefined) {
        searchParams.append('salary__lte', params.salary__lte.toString());
      }

      // Only add '?' if we have params
      if (searchParams.toString()) {
        url = `${url}?${searchParams.toString()}`;
      }
    }
    const response = await sendRequest(ApiMethod.GET, url);

    return response.data;
  };

  const getResources = async (params?: {
    page?: number;
    search?: string;
    page_size?: number;
    category?: string;
    is_featured?: string;
  }) => {
    let url = routes.content.resources;

    if (params) {
      const searchParams = new URLSearchParams();

      if (params.page) {
        searchParams.append('page', params.page.toString());
      }

      if (params.page_size) {
        searchParams.append('page_size', params.page_size.toString());
      }

      if (params.search) {
        searchParams.append('search', params.search);
      }

      if (params.category) {
        searchParams.append('category', params.category);
      }

      if (params.is_featured) {
        searchParams.append('is_featured', params.is_featured);
      }

      // Only add '?' if we have params
      if (searchParams.toString()) {
        url = `${url}?${searchParams.toString()}`;
      }
    }
    const response = await sendRequest(ApiMethod.GET, url);

    return response.data;
  };

  const getTools = async (params?: {
    page?: number;
    page_size?: number;
    search?: string;
    category?: string;
  }) => {
    let url = routes.content.resources;

    if (params) {
      const searchParams = new URLSearchParams();

      if (params.page) {
        searchParams.append('page', params.page.toString());
      }

      if (params.page_size) {
        searchParams.append('page_size', params.page_size.toString());
      }

      if (params.search) {
        searchParams.append('search', params.search);
      }

      if (params.category) {
        searchParams.append('category', params.category);
      }

      // Only add '?' if we have params
      if (searchParams.toString()) {
        url = `${url}?${searchParams.toString()}`;
      }
    }
    const response = await sendRequest(ApiMethod.GET, url);

    return response.data;
  };

  const getCategoryDetail = async (slug: string) => {
    const url = routes.content.byCategory(slug);
    const response = await sendRequest(ApiMethod.GET, url);

    return response.data;
  };

  const getJobDetail = async (jobId: string) => {
    const url = routes.content.byJob(jobId);
    const response = await sendRequest(ApiMethod.GET, url);

    return response.data;
  };

  const getEventDetail = async (eventId: string) => {
    const url = routes.content.byEvent(eventId);
    const response = await sendRequest(ApiMethod.GET, url);

    return response.data;
  };

  const getResourceDetail = async (resourceId: string) => {
    const url = routes.content.byResource(resourceId);
    const response = await sendRequest(ApiMethod.GET, url);

    return response.data;
  };

  const getToolDetail = async (toolId: string) => {
    const url = routes.content.byTool(toolId);
    const response = await sendRequest(ApiMethod.GET, url);

    return response.data;
  };

  const getArticles = async (params?: {
    page?: number;
    page_size?: number;
    tag?: string;
    search?: string;
    ordering?: string;
  }) => {
    let url = routes.article.articles;

    if (params) {
      const searchParams = new URLSearchParams();

      if (params.page) {
        searchParams.append('page', params.page.toString());
      }

      if (params.page_size) {
        searchParams.append('page_size', params.page_size.toString());
      }

      if (params.tag) {
        searchParams.append('tags__name', params.tag);
      }

      if (params.search) {
        searchParams.append('search', params.search);
      }

      if (params.ordering) {
        searchParams.append('ordering', params.ordering);
      }

      if (searchParams.toString()) {
        url = `${url}?${searchParams.toString()}`;
      }
    }

    const response = await sendRequest(ApiMethod.GET, url);
    return response.data;
  };

  const getArticleDetail = async (username: string, slug: string) => {
    const url = routes.article.byArticle(username, slug);
    const response = await sendRequest(ApiMethod.GET, url);

    return response.data;
  };

  const acceptGuidelines = async (
    userIsNotAuthenticatedCallback: () => void,
    termsAccepted: boolean = true
  ) => {
    const url = routes.content.contribute;
    const response = await sendAuthGuardedRequest(
      userIsNotAuthenticatedCallback,
      ApiMethod.POST,
      url,
      {
        terms_accepted: termsAccepted,
      }
    );
    return response;
  };

  return {
    getResources,
    getEvents,
    getJobs,
    getTools,
    getCategories,
    getArticles,
    getCategoryDetail,
    getJobDetail,
    getEventDetail,
    getResourceDetail,
    getToolDetail,
    getArticleDetail,
    acceptGuidelines,
  };
};
