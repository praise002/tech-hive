import PropTypes from 'prop-types';
import ArticleCard from '../common/ArticleCard';
import Text from '../common/Text';
import { displayedArticles } from '../../data/articles';
import { Link } from 'react-router-dom';
import { useState } from 'react';

function Articles({ marginTop = 20, showAdminActions }) {
  const [openArticleId, setOpenArticleId] = useState(null);

  function handleMenuClick(articleId) {
    setOpenArticleId((prevId) => (prevId === articleId ? null : articleId));
  }

  return (
    <div
      className={`lg:mt-4 max-w-7xl mx-auto px-4 lg:px-8 mb-4 mt-${marginTop}`}
    >
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
            className="cursor-pointer text-secondary hover:text-red transition-colors"
          >
            See all
          </Link>
        </div>
      </div>
      <div>
        <div className="grid grid-cols-1 md:grid-cols-2 2xl:grid-cols-4 gap-4 h-full">
          {/* <div className="flex flex-col gap-y-2"> */}
          {displayedArticles.map((article) => (
            <ArticleCard
              showAdminActions={showAdminActions}
              key={article.id}
              article={article}
              isOpen={openArticleId === article.id}
              onMenuClick={handleMenuClick}
            />
          ))}
        </div>
      </div>
    </div>
  );
}

Articles.propTypes = {
  marginTop: PropTypes.string,
  showAdminActions: PropTypes.bool,
};

export default Articles;
