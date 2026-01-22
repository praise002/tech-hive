import { useState } from 'react';
import { MdOutlineAddReaction, MdAddReaction } from 'react-icons/md';
import { useCurrentUser } from '../../features/profile/hooks/useProfile';
import { useAuthModal } from '../../context/AuthModalContext';
import {
  useToggleArticleReaction,
  useArticleReactionStatistics,
} from '../../features/articles/hooks/useArticle';
import { ReactionType } from '../../types/article';

interface ReactionProps {
  articleId: string;
}

const SUPPORTED_REACTIONS: { id: ReactionType; emoji: string }[] = [
  { id: '❤️', emoji: '❤️' },
  { id: '👍', emoji: '👍' },
  { id: '🔥', emoji: '🔥' },
  { id: '😍', emoji: '😍' },
];

function Reaction({ articleId }: ReactionProps) {
  const [showReactions, setShowReactions] = useState(false); // Shows or hides the list of emojis
  const [hoveredId, setHoveredId] = useState<string | null>(null); // Remembers which emoji you're hovering over with your mouse
  const { isAuthenticated } = useCurrentUser();
  const { openAuthModal } = useAuthModal();

  const { data: stats } = useArticleReactionStatistics(articleId);
  const { toggleArticleReaction, isPending: isToggling } =
    useToggleArticleReaction();

  // Derived state from API data
  const userReactions = stats?.user_reactions || [];
  const reactionCounts = stats?.reaction_counts || {};
  const totalReactions = stats?.total_reactions || 0;

  // Check if user has reacted
  const hasUserReacted =
    Array.isArray(userReactions) && userReactions.length > 0;
  function handleToggleReaction(reactionType: ReactionType) {
    if (!isAuthenticated) {
      openAuthModal(window.location.pathname);
      return;
    }

    toggleArticleReaction(
      { articleId, reactionType },
      {
        onSuccess: () => {
          setShowReactions(false);
        },
      }
    );
  }

  // Close dropdown when clicking existing reaction button if it's open, or toggle it
  const toggleDropdown = () => setShowReactions((prev) => !prev);

  return (
    <div className="relative">
      <div className="inline-flex flex-col gap-1">
        <button
          className="hover:opacity-80 transition cursor-pointer min-w-[48px] min-h-[48px] flex items-center justify-center"
          onClick={toggleDropdown}
          aria-haspopup="true"
          aria-expanded={showReactions}
          disabled={isToggling}
        >
          {hasUserReacted ? (
            <MdAddReaction
              className="w-6 h-6  dark:text-custom-white"
              aria-hidden="true"
            />
          ) : (
            <MdOutlineAddReaction
              className="w-6 h-6 dark:text-custom-white"
              aria-hidden="true"
            />
          )}
        </button>
        <span
          className="dark:text-custom-white text-center text-sm"
          aria-label={`Total reactions: ${totalReactions}`}
        >
          {totalReactions}
        </span>
      </div>

      {showReactions && (
        <div
          className="px-1 flex absolute -top-7 left-8 mt-2 bg-white dark:bg-dark border border-gray dark:border-0 rounded-2xl shadow-lg p-2 z-10"
          role="menu"
          aria-label="Pick a reaction"
        >
          {SUPPORTED_REACTIONS.map((reaction) => {
            const count = reactionCounts[reaction.id] || 0;
            const isSelected = userReactions.includes(reaction.id);

            return (
              <div
                key={reaction.id}
                className="relative dark:text-custom-white rounded-md px-1 flex flex-col gap-x-8 items-center"
                onMouseEnter={() => setHoveredId(reaction.id)}
                onMouseLeave={() => setHoveredId(null)}
                onClick={() => handleToggleReaction(reaction.id)}
              >
                <button
                  className="cursor-pointer hover:scale-125 transition-transform"
                  aria-label={`React with ${reaction.id} emoji`}
                  aria-pressed={isSelected}
                  role="menuitem"
                  disabled={isToggling}
                >
                  <span className="w-6 h-6" aria-hidden="true">
                    {reaction.emoji}
                  </span>
                  <span
                    className="text-xs"
                    aria-label={`${count} ${reaction.id} reactions`}
                  >
                    {' '}
                    {count}
                  </span>
                </button>

                {hoveredId === reaction.id && (
                  <div
                    className="absolute -top-8 left-1/2 -translate-x-1/2 px-2 py-1 bg-black text-custom-white text-xs rounded whitespace-nowrap"
                    role="tooltip"
                  >
                    {reaction.id}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

export default Reaction;
