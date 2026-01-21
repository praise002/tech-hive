import { useUserArticles } from '../hooks/useProfile';
import ProfileArticleList from './ProfileArticleList';

function DraftsContent() {
  const { isPending, isError, articles } = useUserArticles({ status: 'draft' });

  return (
    <ProfileArticleList
      isLoading={isPending}
      isError={isError}
      articles={articles}
      emptyMessage="You have no drafts."
      title="My Drafts"
    />
  );
}

export default DraftsContent;
