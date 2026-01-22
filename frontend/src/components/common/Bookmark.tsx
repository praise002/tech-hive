import { FaRegBookmark } from 'react-icons/fa6';
import { FaBookmark } from 'react-icons/fa';
import { useEffect, useState } from 'react';
import { toast } from 'react-hot-toast';
import { BookmarkProps } from '../../types/types';
import { Article } from '../../types/article';
import {
  useCurrentUser,
  useUpdateSavedArticle,
  useUserSavedArticles,
} from '../../features/profile/hooks/useProfile';
import { useAuthModal } from '../../context/AuthModalContext';

function Bookmark({ className = '', articleId }: BookmarkProps) {
  const [isBookmarked, setIsBookmarked] = useState(false);
  const { isAuthenticated } = useCurrentUser();
  const { openAuthModal } = useAuthModal();

  const { articles: savedArticles, isPending: isCheckingSaved } =
    useUserSavedArticles();

  useEffect(() => {
    if (Array.isArray(savedArticles) && articleId) {
      const isSaved = savedArticles.some(
        (savedItem: { article: Article }) => savedItem.article.id === articleId
      );
      setIsBookmarked(isSaved);
    }
  }, [savedArticles, articleId]);

  const handleUnauthenticated = () => {
    openAuthModal(window.location.pathname);
  };

  const { updateSavedArticle, isPending } = useUpdateSavedArticle(
    handleUnauthenticated
  );

  const handleBookmarkClick = () => {
    if (!isAuthenticated) {
      openAuthModal(window.location.pathname);
      return;
    }

    // Optimistic update
    const newStatus = !isBookmarked;
    setIsBookmarked(newStatus);

    updateSavedArticle(
      { article_id: articleId },
      {
        onSuccess: () => {
          toast.success(
            newStatus
              ? 'Article saved to bookmarks'
              : 'Article removed from bookmarks'
          );
        },
        onError: () => {
          // Revert on error
          setIsBookmarked(!newStatus);
          toast.error('Failed to update bookmark');
        },
      }
    );
  };

  return (
    <button
      onClick={handleBookmarkClick}
      disabled={isPending || isCheckingSaved}
      aria-label={isBookmarked ? 'Remove bookmark' : 'Add bookmark'}
      className="focus:outline-none transition-transform active:scale-95"
    >
      {isBookmarked ? (
        <FaBookmark className={`cursor-pointer text-primary ${className}`} />
      ) : (
        <FaRegBookmark className={`cursor-pointer ${className}`} />
      )}
    </button>
  );
}

export default Bookmark;
