import { Link } from 'react-router-dom';
import { trendingArticles } from '../../data/articles';
import ArticleCard from '../common/ArticleCard';
import Text from '../common/Text';

function TrendingArticles() {
  return (
    <div className="mt-20 lg:mt-4 max-w-7xl mx-auto px-4 lg:px-8 mb-4">
      <div className="flex justify-between items-center">
        <div className="my-4">
          <Text variant="h3" size="xl" className="sm:2xl">
            Trending Articles
          </Text>
          <div className="w-[20px]">
            <hr className="border-b-2 border-[#a32816]" />
          </div>
        </div>
        <div>
          <Link
            to="articles"
            className="cursor-pointer text-[#889392] hover:text-[#a32816] transition-colors"
          >
            See all
          </Link>
        </div>
      </div>
      <div>
        <div className="grid grid-cols-1 md:grid-cols-2 2xl:grid-cols-4 gap-4 h-full">
          {trendingArticles.map((article) => (
            <ArticleCard key={article.title} article={article} />
          ))}
        </div>
      </div>
    </div>
  );
}

export default TrendingArticles;
