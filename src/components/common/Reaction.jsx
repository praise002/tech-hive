import { useState } from 'react';
import { MdOutlineAddReaction } from 'react-icons/md';

const reactions = [
  { id: 'Like', emoji: '👍', numReactions: 3 }, // backend updates numReactions
  { id: 'Love', emoji: '❤️', numReactions: 5 },
  { id: 'Laugh', emoji: '😄', numReactions: 9 },
  { id: 'Think', emoji: '🤔', numReactions: 13 },
  { id: 'Angry', emoji: '😡', numReactions: 1 },
];

function Reaction() {
  const [selectedReaction, setSelectedReaction] = useState(null);
  const [showReactions, setShowReactions] = useState(false); // Show reactions on hover
  const [hoveredId, setHoveredId] = useState(null); // Stores the ID of the reaction currently being hovered

  function toggleReaction(reactionId) {
    setSelectedReaction((currentReaction) =>
      currentReaction === reactionId ? null : reactionId
    );
    setShowReactions(false); // Hide reaction picker after selection
  }

  // Get the selected reaction emoji
  const selectedEmoji = reactions.find((r) => r.id === selectedReaction)?.emoji;

  return (
    <div className="relative">
      <button
        className="hover:opacity-80 transition cursor-pointer"
        onClick={() => setShowReactions((show) => !show)}
      >
        {selectedEmoji ? (
          <span className='text-xl sm:text-2xl'>{selectedEmoji}</span>
        ) : (
          <MdOutlineAddReaction className="w-6 h-6 dark:text-custom-white" />
        )}
      </button>

      {showReactions && (
        <div className="px-1 flex absolute -top-7 left-8 mt-2 bg-white dark:bg-dark border border-gray dark:border-0 rounded-2xl shadow-lg p-2 z-10">
          {reactions.map((reaction) => (
            <div
              key={reaction.id}
              className="relative dark:text-custom-white rounded-md px-1 flex flex-col gap-x-8 items-center"
              onMouseEnter={() => setHoveredId(reaction.id)}
              onMouseLeave={() => setHoveredId(null)} // reset
              onClick={() => toggleReaction(reaction.id)}
            >
              <button className="cursor-pointer hover:scale-125 transition-transform">
                <span>{reaction.emoji}</span>
                <span className="text-xs"> {reaction.numReactions}</span>
              </button>

              {hoveredId === reaction.id && (
                <div className="absolute -top-8 left-1/2 -translate-x-1/2 px-2 py-1 bg-black text-custom-white text-xs rounded whitespace-nowrap">
                  {reaction.id}
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Display Selected Reactions */}
      {/* <div className="flex gap-2 mt-2">
        {reactions.map((reaction) => {
          return (
            <span key={reaction.id} className="text-xl">
              {reaction.emoji}
            </span>
          );
        })}
      </div> */}
    </div>
  );
}

export default Reaction;
