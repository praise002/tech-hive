import { useApi } from '../features/auth/hooks/useApi';
import { ApiMethod } from '../types/auth';
import { routes } from '../utils/constants';

export const useContentApi = () => {
  const { sendRequest } = useApi();

  const getCategories = async () => {
    const response = await sendRequest(
      ApiMethod.GET,
      routes.content.categories
    );

    return response.data;
  };

  const getEvents = async () => {
    const response = await sendRequest(ApiMethod.GET, routes.content.events);

    return response.data;
  };

  const getJobs = async () => {
    const response = await sendRequest(ApiMethod.GET, routes.content.jobs);

    return response.data;
  };

  const getResources = async () => {
    const response = await sendRequest(ApiMethod.GET, routes.content.resources);

    return response.data;
  };

  const getTools = async () => {
    const response = await sendRequest(ApiMethod.GET, routes.content.tools);

    return response.data;
  };

  return {
    getCategories,
    getEvents,
    getJobs,
    getResources,
    getTools,
  };
};
