import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { ErrorBoundary } from 'react-error-boundary';

import './index.css';
import App from './App.jsx';
import ErrorFallbacks from './components/common/ErrorFallbacks.jsx';

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
      <App />
      {/* <BuggyComponent /> */}
    </ErrorBoundary>
  </StrictMode>
);
