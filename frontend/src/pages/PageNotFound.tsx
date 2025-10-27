import { useMoveBack } from '../hooks/useMoveBack';

function PageNotFound() {
  const moveBack = useMoveBack();

  return (
    <main className="px-2 sm:px-0 min-h-screen flex flex-col items-center justify-center bg-gray-100">
      <h1 className="text-4xl font-bold text-gray-800 mb-4">
        404 - Page Not Found
      </h1>
      <p className="text-gray-600 mb-8">
        The page you&apos;re looking for doesn&apos;t exist or has been moved.
      </p>
      <button
        className="min-w-[48px] min-h-[48px] bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        onClick={moveBack}
        aria-label="Go back to previous page"
      >
        &larr; Go back
      </button>
    </main>
  );
}

export default PageNotFound;
