import { useApi } from '../features/auth/hooks/useApi';
import { ApiMethod } from '../types/auth';
import { routes } from '../utils/constants';

export const useContentApi = () => {
  const { sendRequest } = useApi();

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

  const getEvents = async (params?: { page?: number; page_size?: number }) => {
    let url = routes.content.events;

    if (params) {
      const searchParams = new URLSearchParams();

      if (params.page) {
        searchParams.append('page', params.page.toString());
      }

      if (params.page_size) {
        searchParams.append('page_size', params.page_size.toString());
      }

      // Only add '?' if we have params
      if (searchParams.toString()) {
        url = `${url}?${searchParams.toString()}`;
      }
    }
    const response = await sendRequest(ApiMethod.GET, url);

    return response.data;
  };

  const getJobs = async (params?: { page?: number; page_size?: number }) => {
    let url = routes.content.jobs;

    if (params) {
      const searchParams = new URLSearchParams();

      if (params.page) {
        searchParams.append('page', params.page.toString());
      }

      if (params.page_size) {
        searchParams.append('page_size', params.page_size.toString());
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
    page_size?: number;
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

      // Only add '?' if we have params
      if (searchParams.toString()) {
        url = `${url}?${searchParams.toString()}`;
      }
    }
    const response = await sendRequest(ApiMethod.GET, url);

    return response.data;
  };

  const getTools = async (params?: { page?: number; page_size?: number }) => {
    let url = routes.content.resources;

    if (params) {
      const searchParams = new URLSearchParams();

      if (params.page) {
        searchParams.append('page', params.page.toString());
      }

      if (params.page_size) {
        searchParams.append('page_size', params.page_size.toString());
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

  return {
    getResources,
    getEvents,
    getJobs,
    getTools,
    getCategories,
    getCategoryDetail,
    getJobDetail,
    getEventDetail,
    getResourceDetail,
    getToolDetail,
  };
};
