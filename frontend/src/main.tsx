import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { ErrorBoundary } from 'react-error-boundary';

import 'react-image-crop/dist/ReactCrop.css';
import './index.css';
import App from './App';
import 'highlight.js/styles/atom-one-dark.css';
import ErrorFallback from './components/common/ErrorFallback';
import ThemeProvider from './context/ThemeProvider';

// function BuggyComponent() {
//   // Simulate a runtime error
//   throw new Error("Oops! Something went wrong.");

// }

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ErrorBoundary
      FallbackComponent={ErrorFallback}
      onReset={() => window.location.replace('/')}
    >
      <ThemeProvider>
        <App />
      </ThemeProvider>

      {/* <BuggyComponent /> */}
    </ErrorBoundary>
  </StrictMode>
);
