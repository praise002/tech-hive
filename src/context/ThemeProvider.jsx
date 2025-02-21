import { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import { ThemeContext } from './ThemeContext';

// Create the provider
function ThemeProvider({ children }) {
  const [theme, setTheme] = useState(() => {
    // Check if the user has a saved preference in localStorage
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) return savedTheme;

    // Otherwise, check the system preference
    return window.matchMedia('(prefers-color-scheme: dark)').matches
      ? 'dark'
      : 'light';
  });

  // Function to toggle theme
  function toggleTheme() {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
    localStorage.setItem('theme', newTheme); // Persist the theme
  }

  // Apply the theme to the <html> element
  useEffect(() => {
    document.documentElement.classList.toggle('dark', theme === 'dark');
  }, [theme]);

  const contextValue = { theme, toggleTheme };

  return (
    <ThemeContext.Provider value={contextValue}>
      {children}
    </ThemeContext.Provider>
  );
}

ThemeProvider.propTypes = {
  children: PropTypes.node.isRequired,
};

export default ThemeProvider;
