import { CommentCreateRequest } from '../../../types/article';
import { ApiMethod } from '../../../types/auth';
import { routes } from '../../../utils/constants';
import { useApi } from '../../auth/hooks/useApi';

export const useArticleApi = () => {
  const { sendRequest, sendAuthGuardedRequest } = useApi();

  const getArticles = async (params?: {
    limit?: number;
    page?: number;
    page_size?: number;
    is_featured?: number;
    search?: number;
  }) => {
    let url = routes.article.articles;

    if (params) {
      const searchParams = new URLSearchParams();

      if (params.limit) {
        searchParams.append('limit', params.limit.toString());
      }

      if (params.page) {
        searchParams.append('page', params.page.toString());
      }

      if (params.page_size) {
        searchParams.append('page_size', params.page_size.toString());
      }

      if (params.is_featured) {
        searchParams.append('is_featured', params.is_featured.toString());
      }

      if (params.search) {
        searchParams.append('search', params.search.toString());
      }

      // Only add '?' if we have params
      if (searchParams.toString()) {
        url = `${url}?${searchParams.toString()}`;
      }
    }
    const response = await sendRequest(ApiMethod.GET, url);

    return response.data;
  };

  const getArticleDetail = async (username: string, slug: string) => {
    const articleDetail = routes.article.byArticle(username, slug);
    const response = await sendRequest(ApiMethod.GET, articleDetail);

    return response.data;
  };

  const getTags = async (params?: {
    page?: number;
    page_size?: number;
    limit?: number;
    search?: string;
  }) => {
    let url = routes.article.articles;
    if (params) {
      const searchParams = new URLSearchParams();

      if (params.limit) {
        searchParams.append('limit', params.limit.toString());
      }

      if (params.search) {
        searchParams.append('search', params.search);
      }

      if (searchParams.toString()) {
        url = `${url}?${searchParams.toString()}`;
      }
    }

    const response = await sendRequest(ApiMethod.GET, url);
    return response.data;
  };

  // CREATE COMMENT (root or reply)
  const createComment = async (
    userIsNotAuthenticatedCallback: () => void,
    data: CommentCreateRequest
  ) => {
    const url = routes.article.comments;
    const response = await sendAuthGuardedRequest(
      userIsNotAuthenticatedCallback,
      ApiMethod.POST,
      url,
      data
    );
    return response.data;
  };

  const getThreadReplies = async (commentId: string) => {
    const url = routes.article.commentReplies(commentId);
    const response = await sendRequest(ApiMethod.GET, url);
    return response.data;
  };

  const deleteComment = async (
    userIsNotAuthenticatedCallback: () => void,
    commentId: string
  ) => {
    const url = routes.article.commentById(commentId);
    const response = await sendAuthGuardedRequest(
      userIsNotAuthenticatedCallback,
      ApiMethod.DELETE,
      url
    );
    console.log(response.data);
    return true;
  };

  const toggleCommentLike = async (
    userIsNotAuthenticatedCallback: () => void,
    commentId: string
  ) => {
    const url = routes.article.commentLike(commentId);
    const response = await sendAuthGuardedRequest(
      userIsNotAuthenticatedCallback,
      ApiMethod.POST,
      url
    );
    return response.data;
  };

  const getCommentLikeStatus = async (commentId: string) => {
    const url = routes.article.commentLikes(commentId);
    const response = await sendRequest(ApiMethod.GET, url);
    return response.data;
  };

  const generateArticleSummary = async (
    userIsNotAuthenticatedCallback: () => void,
    articleId: string,
    forceRegenerate: boolean = false
  ) => {
    const url = routes.article.articleSummary(articleId);
    const params = forceRegenerate ? '?force_regenerate=true' : '';
    const response = await sendAuthGuardedRequest(
      userIsNotAuthenticatedCallback,
      ApiMethod.POST,
      `${url}${params}`
    );
    return response.data;
  };

  const toggleArticleReaction = async (
    userIsNotAuthenticatedCallback: () => void,
    articleId: string,
    reactionType: string // e.g., '❤️', '👍', '🔥'
  ) => {
    const url = routes.article.articleReactions(articleId);
    const response = await sendAuthGuardedRequest(
      userIsNotAuthenticatedCallback,
      ApiMethod.POST,
      url,
      {
        reaction_type: reactionType,
      }
    );
    return response.data;
  };

  const getArticleReactionStatistics = async (articleId: string) => {
    const url = routes.article.articleReactions(articleId);
    const response = await sendRequest(ApiMethod.GET, url);
    return response.data;
  };

  // GET ARTICLE FOR EDITOR (Liveblocks)
  const getArticleEditor = async (
    userIsNotAuthenticatedCallback: () => void,
    articleId: string
  ) => {
    const url = routes.article.articleEditor(articleId);
    const response = await sendAuthGuardedRequest(
      userIsNotAuthenticatedCallback,
      ApiMethod.GET,
      url
    );
    return response.data;
  };

  // SUBMIT ARTICLE FOR REVIEW
  const submitArticle = async (
    userIsNotAuthenticatedCallback: () => void,
    articleId: string
  ) => {
    const url = routes.article.articleSubmit(articleId);
    const response = await sendAuthGuardedRequest(
      userIsNotAuthenticatedCallback,
      ApiMethod.POST,
      url
    );
    return response.data;
  };

  // GET ASSIGNED REVIEWS (for reviewers)
  const getAssignedReviews = async (
    userIsNotAuthenticatedCallback: () => void,
    params?: {
      page?: number;
      page_size?: number;
    }
  ) => {
    let url = routes.article.assignedReviews;

    if (params) {
      const searchParams = new URLSearchParams();

      if (params.page) {
        searchParams.append('page', params.page.toString());
      }

      if (params.page_size) {
        searchParams.append('page_size', params.page_size.toString());
      }

      if (searchParams.toString()) {
        url = `${url}?${searchParams.toString()}`;
      }
    }

    const response = await sendAuthGuardedRequest(
      userIsNotAuthenticatedCallback,
      ApiMethod.GET,
      url
    );
    return response.data;
  };

  const getReviewDetail = async (
    userIsNotAuthenticatedCallback: () => void,
    reviewId: string
  ) => {
    const url = routes.article.reviewById(reviewId);
    const response = await sendAuthGuardedRequest(
      userIsNotAuthenticatedCallback,
      ApiMethod.GET,
      url
    );
    return response.data;
  };

  const startReview = async (
    userIsNotAuthenticatedCallback: () => void,
    reviewId: string
  ) => {
    const url = routes.article.reviewStart(reviewId);
    const response = await sendAuthGuardedRequest(
      userIsNotAuthenticatedCallback,
      ApiMethod.POST,
      url
    );
    return response.data;
  };

  const requestReviewChanges = async (
    userIsNotAuthenticatedCallback: () => void,
    reviewId: string,
    reviewerNotes?: string
  ) => {
    const url = routes.article.reviewRequestChanges(reviewId);
    const response = await sendAuthGuardedRequest(
      userIsNotAuthenticatedCallback,
      ApiMethod.POST,
      url,
      {
        reviewer_notes: reviewerNotes,
      }
    );
    return response.data;
  };

  const approveReview = async (
    userIsNotAuthenticatedCallback: () => void,
    reviewId: string,
    reviewerNotes?: string
  ) => {
    const url = routes.article.reviewApprove(reviewId);
    const response = await sendAuthGuardedRequest(
      userIsNotAuthenticatedCallback,
      ApiMethod.POST,
      url,
      {
        reviewer_notes: reviewerNotes,
      }
    );
    return response.data;
  };

  const rejectReview = async (
    userIsNotAuthenticatedCallback: () => void,
    reviewId: string,
    reviewerNotes?: string
  ) => {
    const url = routes.article.reviewReject(reviewId);
    const response = await sendAuthGuardedRequest(
      userIsNotAuthenticatedCallback,
      ApiMethod.POST,
      url,
      {
        reviewer_notes: reviewerNotes,
      }
    );
    return response.data;
  };

  // LIVEBLOCKS AUTHENTICATION
  const getLiveblocksAuth = async (
    userIsNotAuthenticatedCallback: () => void,
    roomId: string
  ) => {
    const url = routes.article.liveblocksAuth;
    const response = await sendAuthGuardedRequest(
      userIsNotAuthenticatedCallback,
      ApiMethod.POST,
      url,
      {
        room_id: roomId,
      }
    );
    return response.data;
  };

  // SEARCH USERS (for mentions in editor)
  const searchUsers = async (
    userIsNotAuthenticatedCallback: () => void,
    query: string,
    roomId: string
  ) => {
    const url = routes.article.userSearch;
    const params = new URLSearchParams({
      q: query,
      room_id: roomId,
    });
    const response = await sendAuthGuardedRequest(
      userIsNotAuthenticatedCallback,
      ApiMethod.GET,
      `${url}?${params}`
    );
    return response.data;
  };

  // BATCH GET USERS (fetch multiple users by ID)
  const batchGetUsers = async (
    userIsNotAuthenticatedCallback: () => void,
    userIds: string[]
  ) => {
    const url = routes.article.userBatch;
    const response = await sendAuthGuardedRequest(
      userIsNotAuthenticatedCallback,
      ApiMethod.POST,
      url,
      {
        user_ids: userIds,
      }
    );
    return response.data;
  };

  const getRssFeedInfo = async () => {
    const url = routes.article.rssInfo;
    const response = await sendRequest(ApiMethod.GET, url);
    return response.data;
  };

  return {
    getArticles,
    getTags,
    getArticleDetail,
    createComment,
    getThreadReplies,
    deleteComment,
    toggleCommentLike,
    getCommentLikeStatus,
    generateArticleSummary,
    toggleArticleReaction,
    getArticleReactionStatistics,
    getArticleEditor,
    submitArticle,
    getAssignedReviews,
    getReviewDetail,
    startReview,
    requestReviewChanges,
    approveReview,
    rejectReview,
    searchUsers,
    batchGetUsers,
    getLiveblocksAuth,
    getRssFeedInfo,
  };
};
