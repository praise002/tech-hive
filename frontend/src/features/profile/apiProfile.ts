import { UpdateUserData } from '../../types/auth';
import { API_URL } from '../../utils/constants';

export const AUTH_URL = `${API_URL}/auth`;

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
    // TODO: REmove failed to later and put in the usehook - already handles server error
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
