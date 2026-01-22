import { usePublishedArticles } from '../hooks/useProfile';
import ProfileArticleList from './ProfileArticleList';

interface PublishedContentProps {
  username?: string;
}

function PublishedContent({ username }: PublishedContentProps) {
  const { articles, count, isPending, isError } =
    usePublishedArticles(username);

  // Normalize data for ProfileArticleList
  const formattedArticles = {
    results: articles,
    count: count || 0,
  };

  return (
    <div className="mx-auto px-4 lg:px-8 mb-4 mt-8">
      <ProfileArticleList
        isLoading={isPending}
        isError={isError}
        articles={formattedArticles}
        emptyMessage="No published articles found."
        title="Published Articles"
      />
    </div>
  );
}

export default PublishedContent;
