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
    articles: '/articles/',
    events: '/events/',
    jobs: '/jobs/',
    resources: '/resources/',
    tools: '/tools/',
    byArticle: (username: string, slug: string) =>
      `/articles/${username}/${slug}/`,
    byCategory: (slug: string) => `/categories/${slug}/`,
    byJob: (jobId: string) => `/jobs/${jobId}/`,
    byEvent: (eventId: string) => `/events/${eventId}/`,
    byResource: (resourceId: string) => `/resources/${resourceId}/`,
    byTool: (toolId: string) => `/tools/${toolId}/`,
  },

  general: {
    newsletter: '/newsletter/',
  },
};
