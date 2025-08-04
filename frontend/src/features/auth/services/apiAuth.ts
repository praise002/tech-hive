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

export async function register(userData: RegisterUserData): Promise<void> {
  const response = await fetch(`${API_URL}/register/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(userData),
  });

  if (!response.ok) {
    const data = await response.json();
    throw data;
  }

  const data = await response.json();
  localStorage.setItem('email', data.data.email);
  return data;
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
    const data = await response.json();
    throw data;
  }

  const data = await response.json();
  localStorage.setItem('token', data.data.access); // USE HTTP-ONLY LATER
  localStorage.setItem('refresh', data.data.refresh);
  return data;
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
    const data = await response.json();
    throw data;
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

  return await response.json();
}

export async function getCurrentUser() {
  const token = localStorage.getItem('token');
  if (!token) {
    throw new Error('No authentication token found');
  }

  const response = await fetch(`${API_URL}/profile/`, {
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

  return await response.json();
}
