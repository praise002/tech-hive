import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { ErrorBoundary } from 'react-error-boundary';

import './index.css';
import App from './App.jsx';
import 'highlight.js/styles/atom-one-dark.css';
import ErrorFallbacks from './components/common/ErrorFallbacks.jsx';
import ThemeProvider from './context/ThemeProvider.jsx';

// function BuggyComponent() {
//   // Simulate a runtime error
//   throw new Error("Oops! Something went wrong.");

// }

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <ErrorBoundary
      FallbackComponent={ErrorFallbacks}
      onReset={() => window.location.replace('/')}
    >
      <ThemeProvider>
        <App />
      </ThemeProvider>

      {/* <BuggyComponent /> */}
    </ErrorBoundary>
  </StrictMode>
);
