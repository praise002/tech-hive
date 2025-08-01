import { useState } from 'react';
import { MdOutlineAddReaction, MdAddReaction } from 'react-icons/md';

const initialReactions = [
  { id: 'Love', emoji: '❤️', numReactions: 5 },
  { id: 'Laugh', emoji: '😄', numReactions: 9 },
  { id: 'Think', emoji: '🤔', numReactions: 13 },
  { id: 'Angry', emoji: '😡', numReactions: 1 },
  { id: 'Fire', emoji: '🔥', numReactions: 10 },
  { id: 'Heart Eyes', emoji: '😍', numReactions: 4 },
];

function Reaction() {
  const [reactions, setReactions] = useState(initialReactions); // Keeps track of all the reactions and their counts
  const [selectedReactions, setSelectedReactions] = useState<string[]>([]); // Remembers which reactions YOU have selected
  const [showReactions, setShowReactions] = useState(false); // Shows or hides the list of emojis
  const [hoveredId, setHoveredId] = useState<string | null>(null); // Remembers which emoji you're hovering over with your mouse

  function toggleReaction(reactionId: string) {
    setSelectedReactions((prevSelected) => {
      // Check if reaction is already selected
      const isSelected = prevSelected.includes(reactionId);

      return isSelected
        ? // Remove the reaction if already selected
          prevSelected.filter((id) => id !== reactionId)
        : // Add the reaction if not selected
          [...prevSelected, reactionId];
    });

    setReactions((prevReactions) =>
      prevReactions.map((reaction) =>
        reaction.id === reactionId
          ? {
              ...reaction,
              numReactions: selectedReactions.includes(reactionId)
                ? reaction.numReactions - 1
                : reaction.numReactions + 1,
            }
          : reaction
      )
    );

    setShowReactions(false); // Hide reaction picker after selection
  }

  const totalReactions = reactions.reduce(
    (sum, reaction) => sum + reaction.numReactions,
    0
  );

  return (
    <div className="relative">
      <div className="inline-flex flex-col gap-1">
        <button
          className="hover:opacity-80 transition cursor-pointer min-w-[48px] min-h-[48px]"
          onClick={() => setShowReactions((show) => !show)}
          aria-haspopup="true"
          aria-expanded={showReactions}
        >
          {selectedReactions.length > 0 ? (
            <MdAddReaction
              className="w-6 h-6 dark:text-custom-white"
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
          className="dark:text-custom-white"
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
          {reactions.map((reaction) => (
            <div
              key={reaction.id}
              className="relative dark:text-custom-white rounded-md px-1 flex flex-col gap-x-8 items-center"
              onMouseEnter={() => setHoveredId(reaction.id)}
              onMouseLeave={() => setHoveredId(null)} // reset
              onClick={() => toggleReaction(reaction.id)}
            >
              <button
                className="cursor-pointer hover:scale-125 transition-transform"
                aria-label={`React with ${reaction.id} emoji`}
                aria-pressed={selectedReactions.includes(reaction.id)}
                role="menuitem"
              >
                <span className="w-6 h-6" aria-hidden="true">
                  {reaction.emoji}
                </span>
                <span
                  className="text-xs"
                  aria-label={`${reaction.numReactions} ${reaction.id} reactions`}
                >
                  {' '}
                  {reaction.numReactions}
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
          ))}
        </div>
      )}
    </div>
  );
}

export default Reaction;
