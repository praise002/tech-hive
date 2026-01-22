import { useUserArticles } from '../hooks/useProfile';
import ProfileArticleList from './ProfileArticleList';

function SubmittedContent() {
  const { isPending, isError, articles } = useUserArticles({
    status: 'submitted_for_review',
  });

  return (
    <ProfileArticleList
      isLoading={isPending}
      isError={isError}
      articles={articles}
      emptyMessage="No submitted articles found."
      title="Submitted Articles"
    />
  );
}

export default SubmittedContent;
