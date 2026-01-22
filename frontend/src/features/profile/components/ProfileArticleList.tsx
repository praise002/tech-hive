import ArticleCard from '../../../components/common/ArticleCard';
import Spinner from '../../../components/common/Spinner';

import { useState } from 'react';
import { Article } from '../../../types/article';

import Text from '../../../components/common/Text';

interface ProfileArticleListProps {
  isLoading: boolean;
  isError: boolean;
  articles?: {
    results: Article[];
    count: number;
  };
  emptyMessage?: string;
  title?: string;
}

function ProfileArticleList({
  isLoading,
  isError,
  articles,
  emptyMessage = 'No articles found.',
  title,
}: ProfileArticleListProps) {
  const [openArticleId, setOpenArticleId] = useState<string | null>(null);

  function handleMenuClick(articleId: string) {
    setOpenArticleId((prevId) => (prevId === articleId ? null : articleId));
  }

  if (isLoading) {
    return (
      <div className="flex justify-center items-center py-20">
        <Spinner />
      </div>
    );
  }

  if (isError) {
    return (
      <div className="text-center py-20 text-red-600">
        Failed to load articles. Please try again later.
      </div>
    );
  }

  if (!articles?.results?.length) {
    return (
      <div className="text-center py-20 text-secondary">
        <p>{emptyMessage}</p>
      </div>
    );
  }

  return (
    <>
      {title && (
        <Text
          variant="h3"
          size="lg"
          bold={false}
          className="font-semibold mb-4 md:text-2xl dark:text-custom-white"
        >
          {title}
        </Text>
      )}
      <div className="grid grid-cols-1 md:grid-cols-2 2xl:grid-cols-4 gap-4">
        {articles.results.map((article) => (
          <ArticleCard
            key={article.id}
            article={article}
            isOpen={openArticleId === article.id}
            onMenuClick={handleMenuClick}
          />
        ))}
      </div>
    </>
  );
}

export default ProfileArticleList;
