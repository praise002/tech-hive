import {
  ChangePasswordData,
  LoginUserData,
  PasswordResetCompleteData,
  RegisterResponse,
  RegisterUserData,
  UpdateUserData,
  VerifyOtpData,
} from '../../../types/auth';
import { API_URL } from '../../../utils/constants';

export const AUTH_URL = `${API_URL}/auth`;

export async function register(userData: RegisterUserData): Promise<RegisterResponse> {
  const response = await fetch(`${AUTH_URL}/register/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(userData),
  });

  if (!response.ok) {
    const error = await response.json();
    throw error;
  }

  const data = await response.json();
  localStorage.setItem('email', data.data.email);
  return data;
}

export async function verifyRegistrationOtp(otpData: VerifyOtpData) {
  const response = await fetch(`${AUTH_URL}/verification/verify/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(otpData),
  });

  if (!response.ok) {
    const error = await response.json();
    throw error;
  }

  const data = await response.json();
  localStorage.removeItem('email');
  return data;
}

export async function resendRegistrationOtp(email: string) {
  const response = await fetch(`${AUTH_URL}/verification/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw error;
  }

  const data = await response.json();
  localStorage.removeItem('email');
  return data;
}

export async function login(credentials: LoginUserData) {
  const response = await fetch(`${AUTH_URL}/token/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(credentials),
  });

  if (!response.ok) {
    const error = await response.json();
    throw error;
  }

  const data = await response.json();
  localStorage.setItem('token', data.data.access); // USE HTTP-ONLY LATER
  localStorage.setItem('refresh', data.data.refresh);
  return data;
}

export async function logout() {
  const refresh = localStorage.getItem('refresh');
  const response = await fetch(`${AUTH_URL}/sessions/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ refresh }),
  });

  localStorage.removeItem('token');
  localStorage.removeItem('refresh');

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || 'Logout failed');
  }

  return await response.json();
}

export async function logoutAll() {
  const token = localStorage.getItem('token');
  const response = await fetch(`${AUTH_URL}/sessions/all/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
  });

  localStorage.removeItem('token');
  localStorage.removeItem('refresh');

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || 'Logout failed');
  }

  const data = await response.json();
  return data.data;
}

// to display /account
export async function getCurrentUser() {
  const token = localStorage.getItem('token');
  if (!token) {
    throw new Error('No authentication token found');
  }

  const response = await fetch(`${AUTH_URL}/profiles/me/`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    localStorage.removeItem('token');
    localStorage.removeItem('refresh');
    const error = await response.json();
    throw new Error(error.message || 'Failed to fetch user');
  }

  const data = await response.json();
  return data.data;
}

// to display /profile
export async function getCurrentUserProfile() {
  const currentUser = await getCurrentUser();
  const username = currentUser.data.username;
  const token = localStorage.getItem('token');

  const response = await fetch(`${AUTH_URL}/profiles/${username}/`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || 'Failed to get current user profile');
  }

  const data = await response.json();
  return data.data;
}

export async function getUserProfile(username: string) {
  const response = await fetch(`${AUTH_URL}/profiles/${username}/`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || 'Failed to fetch user');
  }

  const data = await response.json();
  return data.data;
}

export async function updateCurrentUserProfile(updateData: UpdateUserData) {
  const token = localStorage.getItem('token');
  if (!token) {
    throw new Error('No authentication token found');
  }

  const response = await fetch(`${AUTH_URL}/profiles/me/`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(updateData),
  });

  if (!response.ok) {
    const error = await response.json();
    throw error;
  }

  const data = await response.json();
  return data.data;
}

export async function updateUserAvatar(avatarFile: File) {
  const token = localStorage.getItem('token');
  if (!token) {
    throw new Error('No authentication token found');
  }

  const formData = new FormData();
  formData.append('avatar', avatarFile);

  const response = await fetch(`${AUTH_URL}/profiles/avatar/`, {
    method: 'PATCH',
    headers: {
      // Don't set Content-Type header - let browser set it with boundary for FormData
      Authorization: `Bearer ${token}`,
    },
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json();
    throw error; // Throw the whole error object for validation errors
  }

  const data = await response.json();
  return data.data;
}

export async function changePassword(passwordData: ChangePasswordData) {
  const token = localStorage.getItem('token');
  if (!token) {
    throw new Error('No authentication token found');
  }

  const response = await fetch(`${AUTH_URL}/passwords/change/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(passwordData),
  });

  if (!response.ok) {
    const error = await response.json();
    throw error;
  }

  const data = await response.json();
  return data;
}

export async function requestPasswordReset(email: string) {
  const response = await fetch(`${AUTH_URL}/passwords/reset/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw error;
  }

  const data = await response.json();

  localStorage.setItem('email', email);

  return data;
}

export async function verifyPasswordResetOtp(otpData: VerifyOtpData) {
  const response = await fetch(`${AUTH_URL}/passwords/reset/verify/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(otpData),
  });

  if (!response.ok) {
    const error = await response.json();
    throw error;
  }

  const data = await response.json();
  localStorage.removeItem('email');
  return data;
}

export async function completePasswordReset(
  resetData: PasswordResetCompleteData
) {
  const response = await fetch(`${AUTH_URL}/passwords/reset/complete/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(resetData),
  });

  if (!response.ok) {
    const error = await response.json();
    throw error;
  }

  const data = await response.json();
  return data;
}

export async function initiateGoogleSignup() {
  const response = await fetch(`${AUTH_URL}/signup/google/`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    const error = await response.json();
    throw error;
  }

  // Step 2: Get Google OAuth URL
  const data = await response.json();
  const googleAuthUrl = data.data.authorization_url;

  // Step 3: Redirect user to Google OAuth page
  window.location.href = googleAuthUrl;
  // User will be redirected to Google, then back to your callback URL
}

export async function initiateGoogleLogin() {
  const response = await fetch(`${AUTH_URL}/login/google/`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    const error = await response.json();
    throw error;
  }

  // Step 2: Get Google OAuth URL
  const data = await response.json();
  const googleAuthUrl = data.data.authorization_url;

  // Step 3: Redirect to Google OAuth
  window.location.href = googleAuthUrl;
}

export async function fetchTokens(state: string, fullUrl: string) {
  if (!state) throw new Error('Missing state');

  
  console.log('Full url for backend: ', fullUrl);
  const apiUrl = new URL(`${AUTH_URL}/google/callback/signup`);
  apiUrl.searchParams.append('state', state);
  apiUrl.searchParams.append('auth_uri', fullUrl);
  console.log('API url for backend: ', apiUrl);

  const response = await fetch(apiUrl);

  if (!response.ok) {
    throw new Error(`HTTP error!  status: ${response.status}`);
  }

  const jsonData = await response.json();
  return jsonData.data;  // Return the data with tokens
}

// TODO: HANDLING GOOGLE CALLBACK FOR FRONTEND NOT TO SEE UGLY DRF SREEN