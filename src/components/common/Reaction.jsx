import { MdOutlineAddReaction } from 'react-icons/md';

const reactions = [
  { id: 'like', emoji: '👍', numReactions: 3 },
  { id: 'love', emoji: '❤️', numReactions: 5 },
  { id: 'laugh', emoji: '😄', numReactions: 9 },
  { id: 'think', emoji: '🤔', numReactions: 13 },
  { id: 'angry', emoji: '😡', numReactions: 1 },
];

function Reaction() {
  return (
    <div className="relative">
      <div>
        <MdOutlineAddReaction className="w-6 h-6 dark:text-custom-white" />
      </div>

      {/* Reaction Picker */}
      <div className="px-1 cursor-pointer flex absolute -top-7 left-8 mt-2 bg-white dark:bg-gray-800 border border-gray dark:border-0 rounded-2xl shadow-lg p-2 z-10">
        {reactions.map((reaction) => (
          <div className="dark:text-custom-white hover:bg-red rounded-md px-1 flex flex-col gap-x-8  items-center" key={reaction.id}>
            <button>{reaction.emoji}</button>
            <button> {reaction.numReactions}</button>
          </div>
        ))}
      </div>

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
