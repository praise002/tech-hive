export const API_URL = 'http://127.0.0.1:9000/api/v1';
// export const API_URL = 'https://252f6a1b6106.ngrok-free.app/api/v1';
// export const API_URL = 'https://tech-hive-production.up.railway.app/api/v1';
export const AUTH_URL = '/auth';
export const PROFILE_URL = '/profiles';

export const routes = {
  auth: {
    register: `${AUTH_URL}/register/`,
    verifyRegOtp: `${AUTH_URL}/verification/verify/`,
    resendRegOtp: `${AUTH_URL}/verification/`,
    login: `${AUTH_URL}/token/`,
    logout: `${AUTH_URL}/sessions/`,
    logoutAll: `${AUTH_URL}/sessions/all/`,
    refreshTokens: `${AUTH_URL}/token/refresh/`,
    changePassword: `${AUTH_URL}/passwords/change/`,
    requestPasswordReset: `${AUTH_URL}/passwords/reset/`,
    verifyPasswordResetOtp: `${AUTH_URL}/passwords/reset/verify/`,
    completePasswordReset: `${AUTH_URL}/passwords/reset/complete/`,
    googleRegister: `${AUTH_URL}/login/google/`,
    googleLogin: `${AUTH_URL}/signup/google/`,
    googleRegsiterCallback: `${AUTH_URL}/google/callback/register/`,
    googleLoginCallback: `${AUTH_URL}/google/callback/login/`,
  },

  profile: {
    me: `${PROFILE_URL}/me/`,
    avatar: `${PROFILE_URL}/avatar/`,
    byUsername: (username: string) => `${PROFILE_URL}/${username}/`,
    articles: `${PROFILE_URL}/articles/`,
    byArticle: (slug: string) => `${PROFILE_URL}/me/${slug}/`,
    saved: `${PROFILE_URL}/me/saved/`,
    comments: `${PROFILE_URL}/me/comments/`,
  },

  content: {
    categories: '/categories/',
    events: '/events/',
    jobs: '/jobs/',
    resources: '/resources/',
    tools: '/tools/',
    comment: '/comments/',
    byCategory: (slug: string) => `/categories/${slug}/`,
    byJob: (jobId: string) => `/jobs/${jobId}/`,
    byEvent: (eventId: string) => `/events/${eventId}/`,
    byResource: (resourceId: string) => `/resources/${resourceId}/`,
    byTool: (toolId: string) => `/tools/${toolId}/`,
  },

  article: {
    articles: '/articles/',
    tags: '/tags/',
    comments: '/comments/',
    assignedReviews: '/reviews/assigned/',
    rssInfo: '/articles/rss/',
    byArticle: (username: string, slug: string) =>
      `/articles/${username}/${slug}/`,

    commentById: (commentId: string) => `/comments/${commentId}/`,
    commentReplies: (commentId: string) => `/comments/${commentId}/replies/`,
    commentLike: (commentId: string) => `/comments/${commentId}/like/`,
    commentLikes: (commentId: string) => `/comments/${commentId}/likes/`,

    articleSummary: (articleId: string) => `/articles/${articleId}/summarize/`,
    articleReactions: (articleId: string) =>
      `/articles/${articleId}/reactions/`,
    articleEditor: (articleId: string) => `/articles/${articleId}/editor/`,
    articleSubmit: (articleId: string) => `/articles/${articleId}/submit/`,

    reviewById: (reviewId: string) => `/reviews/${reviewId}/`,
    reviewStart: (reviewId: string) => `/reviews/${reviewId}/start/`,
    reviewRequestChanges: (reviewId: string) =>
      `/reviews/${reviewId}/request-changes/`,
    reviewApprove: (reviewId: string) => `/reviews/${reviewId}/approve/`,
    reviewReject: (reviewId: string) => `/reviews/${reviewId}/reject/`,

    liveblocksAuth: '/liveblocks/auth/',
    userSearch: '/users/search/',
    userBatch: '/users/batch/',
  },

  general: {
    newsletter: '/newsletter/',
  },
};
