import toast from 'react-hot-toast';

export function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

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

export function clearTokens() {
  const storage = safeLocalStorage();
  storage.removeItem('authTokens');
}

export function setToken(data: object) {
  const storage = safeLocalStorage();
  storage.setItem('authTokens', JSON.stringify(data));
  
}

export function getToken() {
  const storage = safeLocalStorage();
  const authToken = storage.getItem('authTokens');

  if (!authToken) return null;

  const userToken = JSON.parse(authToken);
  return userToken;
}
