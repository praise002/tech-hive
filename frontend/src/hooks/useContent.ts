import { useQuery } from '@tanstack/react-query';
import { useContentApi } from './useContentApi';

export function useCategories() {
  const { getCategories } = useContentApi();

  const {
    isPending,
    data: categories,
    error,
  } = useQuery({
    queryKey: ['categories'],
    queryFn: getCategories,
  });

  return { isPending, error, categories };
}

export function useEvents() {
  const { getEvents } = useContentApi();

  const {
    isPending,
    data: events,
    error,
  } = useQuery({
    queryKey: ['events'],
    queryFn: getEvents,
  });

  return { isPending, error, events };
}

export function useJobs() {
  const { getJobs } = useContentApi();

  const {
    isPending,
    data: jobs,
    error,
  } = useQuery({
    queryKey: ['jobs'],
    queryFn: getJobs,
  });

  return { isPending, error, jobs };
}

export function useResources() {
  const { getResources } = useContentApi();

  const {
    isPending,
    data: resources,
    error,
  } = useQuery({
    queryKey: ['resources'],
    queryFn: getResources,
  });

  return { isPending, error, resources };
}

export function useTools() {
  const { getTools } = useContentApi();

  const {
    isPending,
    data: tools,
    error,
  } = useQuery({
    queryKey: ['tools'],
    queryFn: getTools,
  });

  return { isPending, error, tools };
}
