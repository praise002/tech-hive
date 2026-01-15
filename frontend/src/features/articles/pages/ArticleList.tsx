import { useState } from 'react';
import ArticleCard from '../../../components/common/ArticleCard';
import Button from '../../../components/common/Button';
import Text from '../../../components/common/Text';

import Spinner from '../../../components/common/Spinner';
import { Article } from '../../../types/types';
import { useArticles } from '../../../hooks/useContent';

function ArticleList() {
  const [currentPage, setCurrentPage] = useState(1);
  const { isPending, articles, count, next, previous } = useArticles({
    page_size: 10,
    page: currentPage,
  });
  const totalPages = count ? Math.ceil(count / 10) : 0;

  if (isPending)
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Spinner />
      </div>
    );

  return (
    <div className="pt-20 lg:pt-20 max-w-7xl mx-auto px-4 lg:px-8 mb-4">
      <div className="my-4">
        <Text variant="h3" size="xl" className="sm:2xl dark:text-custom-white">
          All Articles
        </Text>
        <div className="w-[20px]">
          <hr className="border-b-2 border-red" aria-hidden="true" />
        </div>
      </div>
      <ul className="grid grid-cols-1 md:grid-cols-2 2xl:grid-cols-4 gap-4 h-full">
        {articles?.map((article: Article) => (
          <li key={article.id}>
            <ArticleCard article={article} />
          </li>
        ))}
      </ul>

      {/* Static Pagination */}
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

          <span className="text-gray-600" aria-live="polite">
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
    </div>
  );
}

export default ArticleList;
