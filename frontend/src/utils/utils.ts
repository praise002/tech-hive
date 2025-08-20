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
      isAvailable: true
    };
  } catch (e) {
    // localStorage is not available (private browsing, disabled, etc.)
    console.error("Error:", e);
    return {
      setItem: () => {},
      getItem: () => null,
      removeItem: () => {},
      isAvailable: false
    };
  }
}
