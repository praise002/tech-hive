import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useArticleApi } from './useArticleApi';
import { CreateCommentData } from '../../../types/article';
import { useNavigate } from 'react-router-dom';

export function useArticles(params?: {
  limit?: number;
  page?: number;
  page_size?: number;
}) {
  const { getArticles } = useArticleApi();

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

export function useArticleDetail(username: string, slug: string) {
  const { getArticleDetail } = useArticleApi();

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

export function useTags(params?: { limit?: number; search?: string }) {
  const { getTags } = useArticleApi();

  const {
    isPending,
    isError,
    data: tags,
    error,
  } = useQuery({
    queryKey: ['tags', params],
    queryFn: async () => {
      const response = await getTags(params);
      return response;
    },
  });

  return {
    isPending,
    isError,
    tags,
    error,
  };
}

export function useCreateComment() {
  const { createComment: createCommentApi } = useArticleApi();
  const queryClient = useQueryClient();
  const navigate = useNavigate();

  const {
    mutate: createComment,
    isPending,
    isError,
    error,
  } = useMutation({
    mutationFn: (data: CreateCommentData) => {
      const handleUnauthenticated = () => {
        navigate('/login');
      };

      return createCommentApi(handleUnauthenticated, data);
    },

    onSuccess: (variables) => {
      queryClient.invalidateQueries({
        queryKey: ['articleDetail'],
      });

      // If it's a reply, also invalidate the thread replies
      if (variables.thread_id) {
        queryClient.invalidateQueries({
          queryKey: ['threadReplies', variables.thread_id],
        });
      }
    },

    onError: (error) => {
      console.error('Comment update error:', error);
    },
  });

  return { createComment, isPending, isError, error };
}

// This prevents fetching replies for every comment on the page until the user actually
// wants to see them (e.g., clicks "Show replies").
export function useThreadReplies(commentId: string, enabled: boolean = true) {
  const { getThreadReplies } = useArticleApi();

  const {
    isPending,
    isError,
    data: replies,
    error,
  } = useQuery({
    queryKey: ['threadReplies', commentId],
    queryFn: () => getThreadReplies(commentId),
    enabled: enabled && !!commentId, // Only fetch if enabled and commentId exists
  });

  return { isPending, isError, replies: replies || [], error };
}

export function useDeleteComment() {
  const { deleteComment: deleteCommentApi } = useArticleApi();
  const queryClient = useQueryClient();
  const navigate = useNavigate();

  const {
    mutate: deleteComment,
    isPending,
    isError,
    error,
  } = useMutation({
    mutationFn: (commentId: string) => {
      const handleUnauthenticated = () => {
        navigate('/login');
      };

      return deleteCommentApi(handleUnauthenticated, commentId);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['articleDetail'] });
      queryClient.invalidateQueries({ queryKey: ['threadReplies'] });
    },

    onError: (error) => {
      console.error('Comment delete error:', error);
    },
  });

  return { deleteComment, isPending, isError, error };
}

export function useToggleCommentLike() {
  const { toggleCommentLike: toggleCommentLikeApi } = useArticleApi();
  const queryClient = useQueryClient();
  const navigate = useNavigate();

  const {
    mutate: toggleCommentLike,
    isPending,
    isError,
    error,
  } = useMutation({
    mutationFn: (commentId: string) => {
      const handleUnauthenticated = () => {
        navigate('/login');
      };

      return toggleCommentLikeApi(handleUnauthenticated, commentId);
    },
    onSuccess: (data, commentId) => {
      // Update the like status cache
      queryClient.setQueryData(['commentLikeStatus', commentId], data);
      // Also refresh article detail to update like counts
      queryClient.invalidateQueries({ queryKey: ['articleDetail'] });
    },

    onError: (error) => {
      console.error('Comment delete error:', error);
    },
  });
  return { toggleCommentLike, isPending, isError, error };
}

export function useCommentLikeStatus(
  commentId: string,
  enabled: boolean = true
) {
  const { getCommentLikeStatus } = useArticleApi();

  const {
    isPending,
    isError,
    data: likeStatus,
    error,
  } = useQuery({
    queryKey: ['commentLikeStatus', commentId],
    queryFn: () => getCommentLikeStatus(commentId),
    enabled: enabled && !!commentId,
  });

  return { isPending, isError, likeStatus, error };
}

export function useGenerateArticleSummary() {
  const { generateArticleSummary: generateArticleSummaryApi } = useArticleApi();
  const queryClient = useQueryClient();
  const navigate = useNavigate();

  const {
    mutate: generateArticleSummary,
    isPending,
    isError,
    error,
  } = useMutation({
    mutationFn: ({
      articleId,
      forceRegenerate,
    }: {
      articleId: string;
      forceRegenerate?: boolean;
    }) => {
      const handleUnauthenticated = () => {
        navigate('/login');
      };

      return generateArticleSummaryApi(
        handleUnauthenticated,
        articleId,
        forceRegenerate
      );
    },
    onSuccess: (data, variables) => {
      // Cache the summary
      queryClient.setQueryData(['articleSummary', variables.articleId], data);
    },

    onError: (error) => {
      console.error('Generate article summary error:', error);
    },
  });
  return { generateArticleSummary, isPending, isError, error };
}

export function useToggleArticleReaction() {
  const { toggleArticleReaction: toggleArticleReactionApi } = useArticleApi();
  const queryClient = useQueryClient();
  const navigate = useNavigate();

  const {
    mutate: toggleArticleReaction,
    isPending,
    isError,
    error,
  } = useMutation({
    mutationFn: ({
      articleId,
      reactionType,
    }: {
      articleId: string;
      reactionType: string;
    }) => {
      const handleUnauthenticated = () => {
        navigate('/login');
      };

      return toggleArticleReactionApi(
        handleUnauthenticated,
        articleId,
        reactionType
      );
    },
    onSuccess: (data, variables) => {
      // Update reaction status cache
      queryClient.setQueryData(
        ['articleReactionStatus', variables.articleId],
        data
      );
      // Refresh article detail
      queryClient.invalidateQueries({ queryKey: ['articleDetail'] });
    },

    onError: (error) => {
      console.error('Toggle reaction error:', error);
    },
  });
  return { toggleArticleReaction, isPending, isError, error };
}

export function useArticleReactionStatistics(articleId: string) {
  const { getArticleReactionStatistics } = useArticleApi();

  return useQuery({
    queryKey: ['articleReactionStatus', articleId],
    queryFn: () => getArticleReactionStatistics(articleId),
    enabled: !!articleId,
  });
}

export function useArticleEditor(articleId: string) {
  const { getArticleEditor } = useArticleApi();
  const navigate = useNavigate();

  const {
    isPending,
    isError,
    data: article,
    error,
  } = useQuery({
    queryKey: ['articleEditor', articleId],
    queryFn: () => {
      const handleUnauthenticated = () => {
        navigate('/login');
      };
      return getArticleEditor(handleUnauthenticated, articleId);
    },
    enabled: !!articleId,
  });

  return { isPending, isError, article, error };
}

export function useSubmitArticle() {
  const { submitArticle: submitArticleApi } = useArticleApi();
  const queryClient = useQueryClient();
  const navigate = useNavigate();

  const {
    mutate: submitArticle,
    isPending,
    isError,
    error,
  } = useMutation({
    mutationFn: (articleId: string) => {
      const handleUnauthenticated = () => {
        navigate('/login');
      };

      return submitArticleApi(handleUnauthenticated, articleId);
    },
    onSuccess: () => {
      // Refresh user's articles
      queryClient.invalidateQueries({ queryKey: ['userArticle'] });
      // Optionally navigate somewhere
      // navigate('');
    },

    onError: (error) => {
      console.error('Submit article error:', error);
    },
  });
  return { submitArticle, isPending, isError, error };
}

export function useAssignedReviews(params?: {
  page?: number;
  page_size?: number;
}) {
  const { getAssignedReviews } = useArticleApi();
  const navigate = useNavigate();

  const {
    isPending,
    isError,
    data: reviewsResponse,
    error,
  } = useQuery({
    queryKey: ['assignedReviews', params],
    queryFn: () => {
      const handleUnauthenticated = () => {
        navigate('/login');
      };
      return getAssignedReviews(handleUnauthenticated, params);
    },
  });

  const reviews = reviewsResponse?.results || [];
  const count = reviewsResponse?.count;
  const next = reviewsResponse?.next;
  const previous = reviewsResponse?.previous;

  return {
    isPending,
    isError,
    reviews,
    count,
    next,
    previous,
    error,
  };
}

export function useReviewDetail(reviewId: string) {
  const { getReviewDetail } = useArticleApi();
  const navigate = useNavigate();

  const {
    isPending,
    isError,
    data: review,
    error,
  } = useQuery({
    queryKey: ['reviewDetail', reviewId],
    queryFn: () => {
      const handleUnauthenticated = () => {
        navigate('/login');
      };
      return getReviewDetail(handleUnauthenticated, reviewId);
    },

    enabled: !!reviewId,
  });

  return { isPending, isError, review, error };
}

export function useStartReview() {
  const { startReview: startReviewApi } = useArticleApi();
  const queryClient = useQueryClient();

  const navigate = useNavigate();

  const {
    mutate: startReview,
    isPending,
    isError,
    error,
  } = useMutation({
    mutationFn: (reviewId: string) => {
      const handleUnauthenticated = () => {
        navigate('/login');
      };

      return startReviewApi(handleUnauthenticated, reviewId);
    },
    onSuccess: (reviewId) => {
      // Refresh the review detail
      queryClient.invalidateQueries({ queryKey: ['reviewDetail', reviewId] });
      // Refresh assigned reviews list
      queryClient.invalidateQueries({ queryKey: ['assignedReviews'] });
    },

    onError: (error) => {
      console.error('Start review error:', error);
    },
  });
  return { startReview, isPending, isError, error };
}

export function useRequestReviewChanges() {
  const { requestReviewChanges: requestReviewChangesApi } = useArticleApi();
  const queryClient = useQueryClient();
  const navigate = useNavigate();

  const {
    mutate: requestReviewChanges,
    isPending,
    isError,
    error,
  } = useMutation({
    mutationFn: ({
      reviewId,
      reviewerNotes,
    }: {
      reviewId: string;
      reviewerNotes?: string;
    }) => {
      const handleUnauthenticated = () => {
        navigate('/login');
      };

      return requestReviewChangesApi(
        handleUnauthenticated,
        reviewId,
        reviewerNotes
      );
    },
    onSuccess: (variables) => {
      // Refresh review detail
      queryClient.invalidateQueries({
        queryKey: ['reviewDetail', variables.reviewId],
      });
      // Refresh assigned reviews
      queryClient.invalidateQueries({ queryKey: ['assignedReviews'] });
      // Optionally navigate back to reviews list
      // navigate('/dashboard/reviews');
    },

    onError: (error) => {
      console.error('Start review error:', error);
    },
  });
  return { requestReviewChanges, isPending, isError, error };
}

export function useApproveReview() {
  const { approveReview: approveReviewApi } = useArticleApi();
  const queryClient = useQueryClient();
  const navigate = useNavigate();

  const {
    mutate: approveReview,
    isPending,
    isError,
    error,
  } = useMutation({
    mutationFn: ({
      reviewId,
      reviewerNotes,
    }: {
      reviewId: string;
      reviewerNotes?: string;
    }) => {
      const handleUnauthenticated = () => {
        navigate('/login');
      };

      return approveReviewApi(handleUnauthenticated, reviewId, reviewerNotes);
    },
    onSuccess: (variables) => {
      queryClient.invalidateQueries({
        queryKey: ['reviewDetail', variables.reviewId],
      });
      queryClient.invalidateQueries({ queryKey: ['assignedReviews'] });
      // navigate('/dashboard/reviews');
    },

    onError: (error) => {
      console.error('Approve review error:', error);
    },
  });
  return { approveReview, isPending, isError, error };
}

export function useRejectReview() {
  const { rejectReview: rejectReviewApi } = useArticleApi();
  const queryClient = useQueryClient();
  const navigate = useNavigate();

  const {
    mutate: rejectReview,
    isPending,
    isError,
    error,
  } = useMutation({
    mutationFn: ({
      reviewId,
      reviewerNotes,
    }: {
      reviewId: string;
      reviewerNotes?: string;
    }) => {
      const handleUnauthenticated = () => {
        navigate('/login');
      };

      return rejectReviewApi(handleUnauthenticated, reviewId, reviewerNotes);
    },
    onSuccess: (variables) => {
      queryClient.invalidateQueries({
        queryKey: ['reviewDetail', variables.reviewId],
      });
      queryClient.invalidateQueries({ queryKey: ['assignedReviews'] });
      // navigate('/dashboard/reviews');
    },

    onError: (error) => {
      console.error('Start review error:', error);
    },
  });
  return { rejectReview, isPending, isError, error };
}

export function useLiveblocksAuth() {
  const { getLiveblocksAuth } = useArticleApi();
  const navigate = useNavigate();

  const {
    mutate: getLiveblocksAuthToken,
    mutateAsync: getLiveblocksAuthTokenAsync,
    isPending,
    isError,
    error,
  } = useMutation({
    mutationFn: (roomId: string) => {
      const handleUnauthenticated = () => {
        navigate('/login');
      };

      return getLiveblocksAuth(handleUnauthenticated, roomId);
    },
    // No cache invalidation needed - tokens are short-lived
  });

  return {
    getLiveblocksAuthToken,
    getLiveblocksAuthTokenAsync,
    isPending,
    isError,
    error,
  };
}

export function useSearchUsers(
  query: string,
  roomId: string,
  enabled: boolean = true
) {
  const { searchUsers } = useArticleApi();
  const navigate = useNavigate();

  const {
    isPending,
    isError,
    data: users,
    error,
  } = useQuery({
    queryKey: ['userSearch', query, roomId],
    queryFn: () => {
      const handleUnauthenticated = () => {
        navigate('/login');
      };

      return searchUsers(handleUnauthenticated, query, roomId);
    },
    enabled: enabled && !!query && query.length > 0 && !!roomId,
    // Debounce search queries
    staleTime: 30000, // 30 seconds
  });

  return { isPending, isError, users: users || [], error };
}

export function useBatchGetUsers() {
  const { batchGetUsers } = useArticleApi();
  const navigate = useNavigate();

  const {
    mutate: batchGetUsersAction,
    mutateAsync: batchGetUsersAsync,
    isPending,
    isError,
    error,
  } = useMutation({
    mutationFn: (userIds: string[]) => {
      const handleUnauthenticated = () => {
        navigate('/login');
      };

      return batchGetUsers(handleUnauthenticated, userIds);
    },
  });

  return { batchGetUsersAction, batchGetUsersAsync, isPending, isError, error };
}

export function useRssFeedInfo() {
  const { getRssFeedInfo } = useArticleApi();

  const {
    isPending,
    isError,
    data: rssInfo,
    error,
  } = useQuery({
    queryKey: ['rssInfo'],
    queryFn: () => getRssFeedInfo(),
    staleTime: Infinity, // RSS info rarely changes
  });

  return { isPending, isError, rssInfo, error };
}

// enabled: Controls when the query runs (useful for conditional fetching)
// TODO: MOVE THE REDIRECTS TO MUTATE CALLBACKS
