export const API_URL = 'https://127.0.0.1:8000/api/v1';
// export const API_URL = 'https://dc53d894f059.ngrok-free.app/api/v1';
export const AUTH_URL = `${API_URL}/auth`;
export const PROFILE_URL = `${API_URL}/profiles`;

export const routes = {
  auth: {
    me: '/auth/me/',
    register: '/auth/register/',
    verifyRegOtp: '/auth/verification/verify/',
    resendRegOtp: '/auth/verification/',
    login: '/auth/token/',
    logout: '/auth/sessions/',
    logoutAll: '/auth/sessions/all/',
    refreshTokens: '/auth/token/refresh/',
    changePassword: '/auth/passwords/change/',
    requestPasswordReset: '/auth/passwords/reset/',
    verifyPasswordResetOtp: '/auth/passwords/reset/verify/',
    completePasswordReset: '/auth/passwords/reset/complete/',
  },
};
