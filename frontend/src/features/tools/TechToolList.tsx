import { useState } from 'react';
import Button from '../../components/common/Button';
import Text from '../../components/common/Text';
import ToolCard from '../../components/common/ToolCard';
import { useTools } from '../../hooks/useContent';
import Loader from '../../components/common/Loader';
import { ErrorFallbackProps } from '../../types/types';

function TechToolList() {
  const [page, setPage] = useState(1);
  const { tools, isPending, isError, error, next, previous, count } = useTools({
    page,
    page_size: 8,
  });

  if (isPending) {
    return (
      <div className="flex justify-center items-center h-screen">
        <Loader />
      </div>
    );
  }

  if (isError) {
    const errorProps: ErrorFallbackProps = {
      error: error as Error,
    };
    return (
      <div className="text-center py-20 text-red-500">
        Error loading tools: {errorProps.error.message}
      </div>
    );
  }

  return (
    <div className="pt-20 lg:pt-20 max-w-7xl mx-auto px-4 lg:px-8 mb-4">
      <div className="my-4">
        <Text variant="h3" size="xl" className="sm:2xl dark:text-custom-white">
          All Tools
        </Text>
        <div className="w-[20px]" aria-hidden="true">
          <hr className="border-b-2 border-red" />
        </div>
      </div>
      <ul className="grid grid-cols-1 md:grid-cols-2 2xl:grid-cols-4 gap-4 h-full">
        {tools.map((tool: any) => (
          <li key={tool.id}>
            <ToolCard tool={tool} />
          </li>
        ))}
      </ul>

      {/* Pagination */}
      {count > 0 && (
        <nav className="max-w-7xl mx-auto mt-8 flex items-center justify-center">
          <div className="flex items-center space-x-2">
            <Button
              variant="primary"
              aria-label="Go to previous page"
              disabled={!previous}
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              className={!previous ? 'opacity-50 cursor-not-allowed' : ''}
              type="button"
            >
              Previous
            </Button>

            <span className="text-gray-600" aria-live="polite">
              Page {page}
            </span>
            <Button
              variant="primary"
              aria-label="Go to next page"
              disabled={!next}
              onClick={() => setPage((p) => p + 1)}
              className={!next ? 'opacity-50 cursor-not-allowed' : ''}
              type="button"
            >
              Next
            </Button>
          </div>
        </nav>
      )}

      {tools.length === 0 && (
        <div className="text-center py-10 dark:text-custom-white">
          No tools found.
        </div>
      )}
    </div>
  );
}

export default TechToolList;
