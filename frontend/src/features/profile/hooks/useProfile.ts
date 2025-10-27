import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useProfileApi } from './useProfileApi';
import { useNavigate } from 'react-router-dom';
import { UpdateUserData } from '../../../types/auth';

export function useCurrentUser() {
  const { getCurrentUser } = useProfileApi();
  const navigate = useNavigate();

  const {
    isPending,
    data: user,
    error,
  } = useQuery({
    queryKey: ['user'],
    queryFn: () => {
      const handleUnauthenticated = () => {
        navigate('/login');
      };
      return getCurrentUser(handleUnauthenticated);
    },
  });

  const isAuthenticated = user && user.id;

  return { isPending, user, isAuthenticated, error };
}

export function useCurrentUserProfile() {
  const { getCurrentUserProfile } = useProfileApi();
  const navigate = useNavigate();

  const {
    isPending,
    isError,
    data: profile,
    error,
  } = useQuery({
    queryKey: ['profile'],
    queryFn: () => {
      const handleUnauthenticated = () => {
        navigate('/login');
      };
      return getCurrentUserProfile(handleUnauthenticated);
    },
  });

  return { isPending, isError, profile, error };
}

export function useUserProfile(username: string) {
  const { getUserProfileByUsername } = useProfileApi();

  const {
    isPending,
    isError,
    data: profile,
    error,
  } = useQuery({
    queryKey: ['userProfile', username],
    queryFn: () => getUserProfileByUsername(username),
    enabled: !!username, // Only run if username is provided
  });

  return { isPending, isError, profile, error };
}

export function useUpdateUserProfile() {
  const { updateCurrentUserProfile: updateUserProfileApi } = useProfileApi();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const {
    mutate: updateCurrentUserProfile,
    isPending,
    isError,
    error,
  } = useMutation({
    mutationFn: (updateData: UpdateUserData) => {
      const handleUnauthenticated = () => {
        navigate('/login');
      };
      return updateUserProfileApi(handleUnauthenticated, updateData);
    },

    onSuccess: () => {
      // Invalidate and refetch user data
      queryClient.invalidateQueries({ queryKey: ['user'] });
      queryClient.invalidateQueries({ queryKey: ['profile'] });
    },

    onError: (error) => {
      console.error('Profile update error:', error);
    },
  });
  return { updateCurrentUserProfile, isPending, isError, error };
}

export function useUpdateUserAvatar() {
  const { updateCurrentUserAvatar: updateUserAvatarApi } = useProfileApi();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const {
    mutate: updateCurrentUserAvatar,
    isPending,
    isError,
    error,
  } = useMutation({
    mutationFn: (formData: FormData) => {
      const handleUnauthenticated = () => {
        navigate('/login');
      };

      return updateUserAvatarApi(handleUnauthenticated, formData);
    },

    onSuccess: () => {
      // Invalidate and refetch user data
      queryClient.invalidateQueries({ queryKey: ['user'] });
      queryClient.invalidateQueries({ queryKey: ['profile'] });
    },

    onError: (error) => {
      console.error('Profile update error:', error);
    },
  });
  return { updateCurrentUserAvatar, isPending, isError, error };
}

export function useUserArticles() {
  const { getUserArticles } = useProfileApi();
  const navigate = useNavigate();

  const {
    isPending,
    isError,
    data: articles,
    error,
  } = useQuery({
    queryKey: ['userArticles'],
    queryFn: () => {
      const handleUnauthenticated = () => {
        navigate('/login');
      };
      return getUserArticles(handleUnauthenticated);
    },
  });

  return { isPending, isError, articles, error };
}

export function useUserArticleBySlug(slug: string) {
  const { getUserArticleBySlug } = useProfileApi();
  const navigate = useNavigate();

  const {
    isPending,
    isError,
    data: userArticle,
    error,
  } = useQuery({
    queryKey: ['userArticle', slug],
    queryFn: () => {
      const handleUnauthenticated = () => {
        navigate('/login');
      };
      return getUserArticleBySlug(handleUnauthenticated, slug);
    },

    enabled: !!slug, // Only run if slug is provided
  });

  return { isPending, isError, userArticle, error };
}

export function useUpdateUserArticleBySlug() {
  const { updateUserArticleBySlug: updateUserArticleBySlugApi } =
    useProfileApi();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const {
    mutate: updateUserArticleBySlug,
    isPending,
    isError,
    error,
  } = useMutation({
    mutationFn: ({ slug, updateData }: { slug: string; updateData: any }) => {
      const handleUnauthenticated = () => {
        navigate('/login');
      };

      return updateUserArticleBySlugApi(
        handleUnauthenticated,
        slug,
        updateData
      );
    },

    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['userArticle'] });
      queryClient.invalidateQueries({ queryKey: ['userArticles'] });
    },

    onError: (error) => {
      console.error('Article update error:', error);
    },
  });
  return { updateUserArticleBySlug, isPending, isError, error };
}

export function useUserSavedArticles() {
  const { getUserSavedArticles } = useProfileApi();
  const navigate = useNavigate();

  const {
    isPending,
    isError,
    data: articles,
    error,
  } = useQuery({
    queryKey: ['savedArticles'],
    queryFn: () => {
      const handleUnauthenticated = () => {
        navigate('/login');
      };
      return getUserSavedArticles(handleUnauthenticated);
    },
  });

  return { isPending, isError, articles, error };
}

export function useUpdateSavedArticle() {
  const { updateSavedArticle: updateSavedArticleApi } = useProfileApi();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const {
    mutate: updateSavedArticle,
    isPending,
    isError,
    error,
  } = useMutation({
    mutationFn: (updateData: any) => {
      const handleUnauthenticated = () => {
        navigate('/login');
      };

      return updateSavedArticleApi(handleUnauthenticated, updateData);
    },

    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['savedArticles'] });
    },

    onError: (error) => {
      console.error('Saved Article update error:', error);
    },
  });
  return { updateSavedArticle, isPending, isError, error };
}

export function useUserComments() {
  const { getUserComments } = useProfileApi();
  const navigate = useNavigate();

  const {
    isPending,
    isError,
    data: articles,
    error,
  } = useQuery({
    queryKey: ['comments'],
    queryFn: () => {
      const handleUnauthenticated = () => {
        navigate('/login');
      };
      return getUserComments(handleUnauthenticated);
    },
  });

  return { isPending, isError, articles, error };
}

// TODO: MOVE THE REDIRECTS TO MUTATE CALLBACKS
