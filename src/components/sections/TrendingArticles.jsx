import ArticleCard from '../common/ArticleCard';
import Text from '../common/Text';

function TrendingArticles() {
  return (
    <div className="mt-8 max-w-7xl mx-auto px-4 lg:px-8">
      <div className="flex justify-between items-center">
        <div className="my-4">
          <Text variant="h3" size="xl" className="sm:2xl">
            Trending Articles
          </Text>
          <div className="w-[20px]">
            <hr className="border-b-2 border-[#a32816]" />
          </div>
        </div>
        <div className="text-[#889392]">See all</div>
      </div>
      <div>
        <div>
          <ArticleCard />
        </div>
        <div></div>
        <div></div>
      </div>
    </div>
  );
}

export default TrendingArticles;
