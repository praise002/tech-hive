import toast from 'react-hot-toast';

export function safeLocalStorage() {
  try {
    // Test if localStorage is available and working
    const test = 'localStorage-test';
    localStorage.setItem(test, test);
    localStorage.removeItem(test);
    return {
      setItem: (key: string, value: string) => localStorage.setItem(key, value),
      getItem: (key: string) => localStorage.getItem(key),
      removeItem: (key: string) => localStorage.removeItem(key),
      isAvailable: true,
    };
  } catch (e) {
    // localStorage is not available (private browsing, disabled, etc.)
    console.error('Error:', e);
    toast.error(
      'Your browser settings are blocking storage. Some features may not work properly. Try enabling cookies or using a different browser.'
    );
    return {
      setItem: () => {},
      getItem: () => null,
      removeItem: () => {},
      isAvailable: false,
    };
  }
}

export function removeToken() {
  const storage = safeLocalStorage();
  storage.removeItem('token');
}

export function setToken(token: string, refresh: string) {
  const storage = safeLocalStorage();
  storage.setItem('token', token);
  storage.setItem('refresh', refresh);
}

export function getToken() {
  const storage = safeLocalStorage();
  const userToken = storage.getItem('token');
  return userToken;
}
