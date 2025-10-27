import { UpdateUserData } from '../../../types/auth';
import { API_URL } from '../../../utils/constants';

import { getToken } from '../../../utils/utils';

export const AUTH_URL = `${API_URL}/auth`;
export const PROFILE_URL = `${API_URL}/profiles`;

// to display /account
export async function getCurrentUser() {
  const token = getToken();
  if (!token) {
    throw new Error('No authentication token found');
  }

  const response = await fetch(`${PROFILE_URL}/me/`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    const error = await response.json();
    // throw new Error(error.message || 'Failed to fetch user');
    throw error;
  }

  const data = await response.json();
  return data.data;
}

// to display /profile
export async function getCurrentUserProfile() {
  const currentUser = await getCurrentUser();

  const username = currentUser.data.username;
  const token = getToken();

  const response = await fetch(`${PROFILE_URL}/${username}/`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    const error = await response.json();
    // throw new Error(error.message || 'Failed to get current user profile');
    throw error;
    // TODO: REmove failed to later and put in the usehook - already handles server error
  }

  const data = await response.json();
  return data.data;
}

export async function getUserProfile(username: string) {
  const response = await fetch(`${PROFILE_URL}/${username}/`, {
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
  const token = getToken();
  if (!token) {
    throw new Error('No authentication token found');
  }

  const response = await fetch(`${PROFILE_URL}/me/`, {
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
  const token = getToken();
  if (!token) {
    throw new Error('No authentication token found');
  }

  const formData = new FormData();
  formData.append('avatar', avatarFile);

  const response = await fetch(`${PROFILE_URL}/avatar/`, {
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
