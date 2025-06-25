import { ErrorFallbackProps } from '../../types/types';
import Text from './Text';

function ErrorFallback({ error, resetErrorBoundary }: ErrorFallbackProps) {
  return (
    <div className="p-4 bg-red-100 border border-red-400 text-red-700 rounded">
      <Text variant="h2" size="2xl" color="text-red-700">
        Something went wrong!
      </Text>
      <p className="mb-4">{error.message}</p>
      <button
        onClick={resetErrorBoundary}
        className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
      >
        Try Again
      </button>
    </div>
  );
}

export default ErrorFallback;
