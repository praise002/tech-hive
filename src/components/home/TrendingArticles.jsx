import { homePageTrendingArticles } from '../../data/articles';
import ArticleCard from '../common/ArticleCard';
import Button from '../common/Button';
import Text from '../common/Text';

function TrendingArticles() {
  return (
    <div>
      <div className="my-4">
        <Text variant="h3" size="xl" className="sm:2xl">
          Trending Articles
        </Text>
        <div className="w-[20px]">
          <hr className="border-b-2 border-[#a32816]" />
        </div>
      </div>
      <div className="flex flex-col gap-y-2">
        {homePageTrendingArticles.map((article) => (
          <ArticleCard key={article.title} article={article} />
        ))}
      </div>
      <Button className="my-4">Explore More Articles &rarr;</Button>
    </div>
  );
}

export default TrendingArticles;
