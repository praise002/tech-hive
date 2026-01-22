import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useProfileApi } from './useProfileApi';
import { useNavigate } from 'react-router-dom';
import { useArticles } from '../../articles/hooks/useArticle'; // Import useArticles
import {
  CreateArticleData,
  UpdateUserData,
  UsernamesResponse,
} from '../../../types/auth';
import { handleQueryError } from '../../../utils/utils';

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
    enabled: !!localStorage.getItem('authTokens'), // Only run if token exists
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

export function useUserProfile(username?: string) {
  const { getUserProfileByUsername } = useProfileApi();

  const {
    isPending,
    isError,
    data: profile,
    error,
  } = useQuery({
    queryKey: ['userProfile', username],
    queryFn: () => getUserProfileByUsername(username!),
    enabled: !!username, // Only run if username is provided
  });

  return { isPending, isError, profile, error };
}

export function useUpdateUserProfile(handleUnauthenticated: () => void) {
  const { updateCurrentUserProfile: updateUserProfileApi } = useProfileApi();
  const queryClient = useQueryClient();

  const {
    mutate: updateCurrentUserProfile,
    isPending,
    isError,
    error,
  } = useMutation({
    mutationFn: (updateData: UpdateUserData) => {
      return updateUserProfileApi(handleUnauthenticated, updateData);
    },

    onSuccess: () => {
      // Invalidate and refetch user data
      queryClient.invalidateQueries({ queryKey: ['user'] });
      queryClient.invalidateQueries({ queryKey: ['profile'] });
    },
  });
  return { updateCurrentUserProfile, isPending, isError, error };
}

export function useUpdateUserAvatar(handleUnauthenticated: () => void) {
  const { updateCurrentUserAvatar: updateUserAvatarApi } = useProfileApi();
  const queryClient = useQueryClient();

  const {
    mutate: updateCurrentUserAvatar,
    isPending,
    isError,
    error,
  } = useMutation({
    mutationFn: (formData: FormData) => {
      return updateUserAvatarApi(handleUnauthenticated, formData);
    },

    onSuccess: () => {
      // Invalidate and refetch user data
      queryClient.invalidateQueries({ queryKey: ['user'] });
      queryClient.invalidateQueries({ queryKey: ['profile'] });
    },
  });
  return { updateCurrentUserAvatar, isPending, isError, error };
}

export function useUserArticles(params?: {
  status?: string;
  search?: string;
  page?: number;
  page_size?: number;
}) {
  const { getUserArticles } = useProfileApi();
  const navigate = useNavigate();

  const {
    isPending,
    isError,
    data: articles,
    error,
  } = useQuery({
    queryKey: ['userArticles', params], // Include params in queryKey
    queryFn: () => {
      const handleUnauthenticated = () => {
        navigate('/login');
      };
      return getUserArticles(handleUnauthenticated, params);
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

export function useUpdateUserArticleBySlug(handleUnauthenticated: () => void) {
  const { updateUserArticleBySlug: updateUserArticleBySlugApi } =
    useProfileApi();
  const queryClient = useQueryClient();

  const {
    mutate: updateUserArticleBySlug,
    isPending,
    isError,
    error,
  } = useMutation({
    mutationFn: ({
      slug,
      updateData,
    }: {
      slug: string;
      updateData: FormData | { title?: string; content?: string };
    }) => {
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
      handleQueryError(error, 'User Article update');
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

export function useUpdateSavedArticle(handleUnauthenticated: () => void) {
  const { updateSavedArticle: updateSavedArticleApi } = useProfileApi();
  const queryClient = useQueryClient();

  const {
    mutate: updateSavedArticle,
    isPending,
    isError,
    error,
  } = useMutation({
    mutationFn: (updateData: any) => {
      return updateSavedArticleApi(handleUnauthenticated, updateData);
    },

    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['savedArticles'] });
    },

    onError: (error) => {
      handleQueryError(error, 'Saved Article update');
    },
  });
  return { updateSavedArticle, isPending, isError, error };
}

export function useUsernames(params?: {
  page?: number;
  page_size?: number;
  search?: string;
}) {
  const { getUsernames } = useProfileApi();

  const {
    data: usernamesResponse,
    isPending,
    isError,
    error,
  } = useQuery<UsernamesResponse>({
    queryKey: ['usernames', params],
    queryFn: () => getUsernames(params),
  });

  const usernames = usernamesResponse?.results || [];
  const count = usernamesResponse?.count;
  const next = usernamesResponse?.next;
  const previous = usernamesResponse?.previous;

  return {
    usernames,
    count,
    next,
    previous,
    isPending,
    isError,
    error,
  };
}

export function useCreateUserArticle(handleUnauthenticated: () => void) {
  const { createUserArticle: createUserArticleApi } = useProfileApi();
  const queryClient = useQueryClient();

  const {
    mutate: createUserArticle,
    isPending,
    isError,
    error,
    isSuccess,
  } = useMutation({
    mutationFn: (data: CreateArticleData) => {
      return createUserArticleApi(handleUnauthenticated, data);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['userArticles'] });
    },
    onError: (error) => {
      handleQueryError(error, 'Create Article');
    },
  });

  return { createUserArticle, isPending, isError, error, isSuccess };
}

export function useUserComments(params?: {
  page?: number;
  page_size?: number;
}) {
  const { getUserComments } = useProfileApi();
  const navigate = useNavigate();

  const {
    isPending,
    isError,
    data: comments,
    error,
  } = useQuery({
    queryKey: ['userComments', params],
    queryFn: () => {
      const handleUnauthenticated = () => {
        navigate('/login');
      };
      return getUserComments(handleUnauthenticated, params);
    },
  });

  return { isPending, isError, comments, error };
}

export function useDeleteUserComment(handleUnauthenticated: () => void) {
  const { deleteUserComment: deleteUserCommentApi } = useProfileApi();
  const queryClient = useQueryClient();

  const {
    mutate: deleteUserComment,
    isPending,
    isError,
    error,
  } = useMutation({
    mutationFn: (commentId: string) => {
      return deleteUserCommentApi(handleUnauthenticated, commentId);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['userComments'] });
    },
    onError: (error) => {
      handleQueryError(error, 'Delete Comment');
    },
  });

  return { deleteUserComment, isPending, isError, error };
}

export function usePublishedArticles(username?: string) {
  // 1. Fetching for own profile (if no username is provided)
  const isOwnProfile = !username;
  const {
    articles: userArticlesResponse,
    isPending: isUserPending,
    isError: isUserError,
    error: userError,
  } = useUserArticles(
    isOwnProfile
      ? {
          status: 'published',
          page_size: 10,
        }
      : undefined
  );

  // 2. Fetching for another user (if username IS provided)
  const {
    articles: publicArticles,
    count: publicCount,
    isPending: isPublicPending,
    isError: isPublicError,
    error: publicError,
  } = useArticles(
    !isOwnProfile
      ? {
          author__username: username,
          page_size: 10,
        }
      : undefined
  );

  // 3. Normalize return data
  const articles = isOwnProfile
    ? userArticlesResponse?.results || []
    : publicArticles;

  const count = isOwnProfile ? userArticlesResponse?.count : publicCount;
  const isPending = isOwnProfile ? isUserPending : isPublicPending;
  const isError = isOwnProfile ? isUserError : isPublicError;
  const error = isOwnProfile ? userError : publicError;

  return {
    articles,
    count,
    isPending,
    isError,
    error,
  };
}
