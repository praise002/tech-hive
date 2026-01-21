import { Article } from '../../../types/article';
import { useUserSavedArticles } from '../hooks/useProfile';

import ProfileArticleList from './ProfileArticleList';

interface SavedArticleItem {
  id: string;
  article: Article;
}

function SavedContent() {
  const { isPending, isError, articles } = useUserSavedArticles();

  const transformedArticles = articles
    ? {
        results: (articles as any[]).map(
          (item: SavedArticleItem) => item.article
        ),
        count: (articles as any[]).length,
      }
    : undefined;

  return (
    <div className="mx-auto px-4 lg:px-8 mb-4 mt-8">
      <ProfileArticleList
        isLoading={isPending}
        isError={isError}
        articles={transformedArticles}
        emptyMessage="No saved articles found."
        title="Saved Articles"
      />
    </div>
  );
}

export default SavedContent;
