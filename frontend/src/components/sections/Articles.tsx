import ArticleCard from '../common/ArticleCard';
import Text from '../common/Text';

import { Link } from 'react-router-dom';
import { useState } from 'react';
import { displayedArticles } from '../../data/articles';
import { ArticlesProps } from '../../types/types';

function Articles({
  marginTop = 20,
  showAdminActions,
  context,
  visibleHeader = true,
}: ArticlesProps) {
  const [openArticleId, setOpenArticleId] = useState<string | null>(null);

  function handleMenuClick(articleId: string) {
    setOpenArticleId((prevId) => (prevId === articleId ? null : articleId));
  }

  return (
    <section
      className={`lg:mt-4 max-w-7xl mx-auto px-4 lg:px-8 mb-4 mt-${marginTop}`}
    >
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
          {displayedArticles.map((article) => (
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
