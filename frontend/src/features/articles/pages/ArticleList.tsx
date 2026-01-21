import { useState } from 'react';
import ArticleCard from '../../../components/common/ArticleCard';
import Button from '../../../components/common/Button';
import Text from '../../../components/common/Text';

import { SectionSkeleton } from '../../../components/common/Skeletons';
import { useArticles } from '../hooks/useArticle';
import { useSearchParams } from 'react-router-dom';

function ArticleList() {
  const [searchParams] = useSearchParams();
  const searchQuery = searchParams.get('search') || undefined;
  const [currentPage, setCurrentPage] = useState(1);
  const { isPending, articles, count, next, previous } = useArticles({
    page_size: 10,
    page: currentPage,
    search: searchQuery,
  });
  const totalPages = count ? Math.ceil(count / 10) : 0;

  if (isPending) return <SectionSkeleton marginTop={20} />;

  return (
    <div className="pt-20 lg:pt-20 max-w-7xl mx-auto px-4 lg:px-8 mb-4 min-h-screen">
      <div className="my-4">
        <Text variant="h3" size="xl" className="sm:2xl dark:text-custom-white">
          {searchQuery ? `Search results for "${searchQuery}"` : 'All Articles'}
        </Text>
        <div className="w-[20px]">
          <hr className="border-b-2 border-red" aria-hidden="true" />
        </div>
      </div>
      <ul className="grid grid-cols-1 md:grid-cols-2 2xl:grid-cols-4 gap-4 h-full">
        {articles?.map((article) => (
          <li key={article.id}>
            <ArticleCard article={article} />
          </li>
        ))}
      </ul>

      {/* Pagination */}
      {count > 0 && (
        <div className="max-w-7xl mx-auto mt-8 flex items-center justify-center">
          <div className="flex items-center space-x-2">
            <Button
              variant="primary"
              aria-label="Go to previous page"
              disabled={!previous}
              onClick={() => setCurrentPage((p) => p - 1)}
            >
              Previous
            </Button>

            <span
              className="text-gray-600 dark:text-gray-400"
              aria-live="polite"
            >
              Page {currentPage} of {totalPages}
            </span>
            <Button
              variant="primary"
              aria-label="Go to next page"
              disabled={!next}
              onClick={() => setCurrentPage((p) => p + 1)}
            >
              Next
            </Button>
          </div>
        </div>
      )}

      {count === 0 && (
        <div className="text-center py-10 dark:text-custom-white">
          No articles found.
        </div>
      )}
    </div>
  );
}

export default ArticleList;
