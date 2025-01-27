import PropTypes from 'prop-types';

function ErrorFallbacks({ error, resetErrorBoundary }) {
  return (
    <div className="p-4 bg-red-100 border border-red-400 text-red-700 rounded">
      <h2 className="font-bold">Something went wrong!</h2>
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

ErrorFallbacks.propTypes = {
  error: PropTypes.string.isRequired,
  resetErrorBoundary: PropTypes.func,
};

export default ErrorFallbacks;
