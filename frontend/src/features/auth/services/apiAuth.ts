import { API_URL } from '../../../utils/constants';

interface RegisterUserData {
  first_name: string;
  last_name: string;
  email: string;
  password: string;
}

interface LoginUserData {
  email: string;
  password: string;
}

interface UpdateUserData {
  first_name: string;
  last_name: string;
}

export async function register(userData: RegisterUserData): Promise<void> {
  const response = await fetch(`${API_URL}/register/`, {
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
  return data.data;
}

export async function login(credentials: LoginUserData) {
  const response = await fetch(`${API_URL}/token/`, {
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
  return data.data;
}

export async function logout() {
  const refresh = localStorage.getItem('refresh');
  const response = await fetch(`${API_URL}/sessions/`, {
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
  const response = await fetch(`${API_URL}/sessions/all/`, {
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

  const response = await fetch(`${API_URL}/profiles/me/`, {
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

  const response = await fetch(`${API_URL}/profiles/${username}/`, {
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
  const response = await fetch(`${API_URL}/profiles/${username}/`, {
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

  const response = await fetch(`${API_URL}/profiles/me/`, {
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

  const response = await fetch(`${API_URL}/profiles/avatar/`, {
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
