import ArticleCard from '../common/ArticleCard';
import Text from '../common/Text';

import { Link } from 'react-router-dom';
import { useState } from 'react';

import { Article, ArticlesProps } from '../../types/types';

import Spinner from '../common/Spinner';
import { useArticles } from '../../hooks/useContent';

function Articles({
  marginTop = 20,
  showAdminActions,
  context,
  visibleHeader = true,
}: ArticlesProps) {
  const [openArticleId, setOpenArticleId] = useState<string | null>(null);
  const { isPending, articles } = useArticles({ limit: 4 });

  function handleMenuClick(articleId: string) {
    setOpenArticleId((prevId) => (prevId === articleId ? null : articleId));
  }

  if (isPending)
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Spinner />
      </div>
    );

  return (
    <section className={`lg:mt-4  mx-auto px-4 lg:px-8 mb-4 mt-${marginTop}`}>
      {/* max-w-7xl */}
      {visibleHeader && (
        <div className="flex justify-between items-center">
          <div className="my-4">
            <Text
              variant="h3"
              size="xl"
              className="sm:2xl dark:text-custom-white"
            >
              Articles
            </Text>
            <div className="w-[20px]">
              <hr className="border-b-2 border-red" />
            </div>
          </div>
          <div>
            <Link
              to="/articles"
              className="cursor-pointer text-red-800 dark:text-secondary dark:hover:text-whitedark:text-secondary dark:hover:text-white hover:text-red transition-colors"
              aria-label="See all articles"
            >
              See all
            </Link>
          </div>
        </div>
      )}
      <div>
        <ul className="grid grid-cols-1 md:grid-cols-2 2xl:grid-cols-4 gap-4 h-full">
          {/* <div className="flex flex-col gap-y-2"> */}
          {articles?.map((article: Article) => (
            <li key={article.id}>
              <ArticleCard
                showAdminActions={showAdminActions}
                article={article}
                isOpen={openArticleId === article.id}
                onMenuClick={handleMenuClick}
                context={context}
              />
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}

export default Articles;
