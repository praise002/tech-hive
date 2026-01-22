import { useState, useEffect } from 'react';
import { useCurrentUser } from '../../features/profile/hooks/useProfile';
import { useAuthModal } from '../../context/AuthModalContext';
import {
  useToggleCommentLike,
  useCommentLikeStatus,
} from '../../features/articles/hooks/useArticle';
import { useNavigate } from 'react-router-dom';

interface LikeProps {
  commentId: string;
  initialLikeCount?: number;
  initialIsLiked?: boolean;
}

function Like({
  commentId,
  initialLikeCount = 0,
  initialIsLiked = false,
}: LikeProps) {
  const [isLiked, setIsLiked] = useState(initialIsLiked);
  const [likeCount, setLikeCount] = useState(initialLikeCount);
  const { isAuthenticated } = useCurrentUser();
  const { openAuthModal } = useAuthModal();
  const navigate = useNavigate();

  const handleUnauthenticated = () => {
    navigate('/login');
  };

  const { toggleCommentLike, isPending: isToggling } = useToggleCommentLike(
    handleUnauthenticated
  );

  const { likeStatus } = useCommentLikeStatus(commentId);

  useEffect(() => {
    if (likeStatus) {
      setIsLiked(!!likeStatus.is_liked);
      setLikeCount(likeStatus.like_count);
    }
  }, [likeStatus]);

  const handleLikeClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (!isAuthenticated) {
      openAuthModal(window.location.pathname);
      return;
    }

    // Optimistic update
    const newIsLiked = !isLiked;
    setIsLiked(newIsLiked);
    setLikeCount((prev) => (newIsLiked ? prev + 1 : Math.max(0, prev - 1)));

    toggleCommentLike(commentId, {
      onError: () => {
        // Revert on error
        setIsLiked(!newIsLiked);
        setLikeCount((prev) =>
          !newIsLiked ? prev + 1 : Math.max(0, prev - 1)
        );
      },
    });
  };

  return (
    <button
      className="inline-flex gap-1.5 items-center hover:text-primary transition-colors text-secondary"
      onClick={handleLikeClick}
      disabled={isToggling}
      aria-pressed={isLiked}
      aria-label={isLiked ? 'Unlike' : 'Like'}
    >
      <span
        className={
          isLiked
            ? 'text-red-500 scale-110 transition-transform'
            : 'transition-transform'
        }
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          // fill="none"
          fill={isLiked ? 'currentColor' : 'none'}
          viewBox="0 0 24 24"
          strokeWidth={1.5}
          stroke="currentColor"
          className="size-4"
          aria-hidden="true"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12Z"
          />
        </svg>
      </span>
      <span className="text-xs font-medium min-w-[20px] text-left">
        {isLiked ? 'Unlike' : 'Like'}
      </span>
      <span className="text-xs font-medium min-w-[20px] text-left">
        {likeCount > 0 ? likeCount : ''}
      </span>
    </button>
  );
}

export default Like;
