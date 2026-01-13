import toast from 'react-hot-toast';

export function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
}

export function formatDateB(dateString: string) {
  const date = new Date(dateString);
  const now = new Date();
  const diffTime = Math.abs(now.getTime() - date.getTime());
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)); // 1000ms=is

  if (diffDays === 0) return 'today';
  if (diffDays === 1) return 'yesterday';
  if (diffDays < 7) return `${diffDays} days ago`;
  if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;
  if (diffDays < 365) return `${Math.floor(diffDays / 30)} months ago`;
  return `${Math.floor(diffDays / 365)} years ago`;
}

export function getPreviewText(html: string, maxLength: number = 150) {
  const tmp = document.createElement('DIV');
  tmp.innerHTML = html;
  const plainText = tmp.textContent || tmp.innerText || '';

  const trimmedText = plainText.trim();

  if (trimmedText.length <= maxLength) {
    return trimmedText;
  }

  return trimmedText.slice(0, maxLength) + '...';
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

export const handleQueryError = (error: unknown, context?: string) => {
  const message = error instanceof Error ? error.message : 'Unknown error';

  // Development logging
  if (import.meta.env.DEV) {
    console.error(`[${context || 'Query Error'}]:`, error);
  }

  // Production error tracking
  if (import.meta.env.PROD) {
    // Send to your error monitoring service
    // Sentry.captureException(error, { tags: { context } });
  }

  // Optional: User notification
  // You can add toast notifications here if needed
};
