import { useUserArticles } from '../hooks/useProfile';

import ProfileArticleList from './ProfileArticleList';

import { useArticles } from '../../articles/hooks/useArticle';
import { Article } from '../../../types/article';

interface PublishedContentProps {
  username?: string;
}

function PublishedContent({ username }: PublishedContentProps) {
  // If username is provided, we are viewing another user's profile (useArticles with filtering)
  // If not, we are viewing our own profile (useUserArticles)
  const isOwnProfile = !username;

  const {
    isPending: isUserPending,
    isError: isUserError,
    articles: userArticles,
  } = useUserArticles(
    isOwnProfile
      ? {
          status: 'published',
        }
      : undefined
  );

  const {
    isPending: isPublicPending,
    isError: isPublicError,
    articles: publicArticles,
    count: publicCount,
  } = useArticles(
    !isOwnProfile
      ? {
          author__username: username,
          // You might want to handle pagination here properly eventually
          limit: 100, // Fetch reasonable amount for now
        }
      : undefined
  );

  const isPending = isOwnProfile ? isUserPending : isPublicPending;
  const isError = isOwnProfile ? isUserError : isPublicError;

  // Normalize data for ProfileArticleList
  // useUserArticles returns { results: [], count } (from API response)
  // useArticles (hook) returns flat array [], we wrap it to match { results: [], count }
  const articles = isOwnProfile
    ? userArticles
    : { results: publicArticles as Article[], count: publicCount };

  return (
    <div className="mx-auto px-4 lg:px-8 mb-4 mt-8">
      <ProfileArticleList
        isLoading={isPending}
        isError={isError}
        articles={articles}
        emptyMessage="No published articles found."
        title="Published Articles"
      />
    </div>
  );
}

export default PublishedContent;
