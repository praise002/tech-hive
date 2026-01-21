import { Link } from 'react-router-dom';
import ArticleCard from '../common/ArticleCard';
import Text from '../common/Text';

import { SectionSkeleton } from '../common/Skeletons';
import { useArticles } from '../../features/articles/hooks/useArticle';

interface TrendingArticlesProps {
  category?: string;
}

function TrendingArticles({ category }: TrendingArticlesProps) {
  const { articles, isPending } = useArticles({
    limit: 4,
    ordering: '-annotated_reaction_count',
    category,
  });

  if (isPending) return <SectionSkeleton marginTop={20} />;

  return (
    <section className="mt-20 lg:mt-4 max-w-7xl mx-auto px-4 lg:px-8 mb-4">
      <div className="flex justify-between items-center">
        <div className="my-4">
          <Text
            variant="h3"
            size="xl"
            className="sm:2xl dark:text-custom-white"
          >
            Trending Articles
          </Text>
          <div className="w-[20px]">
            <hr className="border-b-2 border-red" />
          </div>
        </div>
        <div>
          <Link
            to="/articles"
            className="cursor-pointer text-red-800 dark:text-secondary dark:hover:text-white hover:text-red transition-colors"
            aria-label="See all trending articles"
          >
            See all
          </Link>
        </div>
      </div>
      <div>
        <ul className="grid grid-cols-1 md:grid-cols-2 2xl:grid-cols-4 gap-4 h-full">
          {articles.map((article) => (
            <li key={article.id}>
              <ArticleCard article={article} />
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}

export default TrendingArticles;
