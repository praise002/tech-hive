import { ArticleReactionsProps } from '../../types/types';
import Bookmark from './Bookmark';

function ArticleReactions({
  reactions,
  reactionsCount,
  posted,
  readTime,
}: ArticleReactionsProps) {
  return (
    <div
      className="flex flex-col"
      role="group"
      aria-label="Article reactions and details"
    >
      {/* Reactions and Bookmark Section */}
      <div className="flex justify-between items-center my-3">
        {/* Reactions */}
        <div className="flex items-center space-x-2">
          <div className="flex space-x-1 text-lg">
            {reactions.map((reaction, index) => (
              <span
                key={index}
                className={`inline-flex items-center justify-center w-6 h-6 rounded-full shadow-md ${
                  index !== 0 ? '-ml-2' : ''
                }`}
                aria-label={`Reaction emoji ${index + 1}`}
              >
                {reaction}
              </span>
            ))}
          </div>
          <div
            className="whitespace-nowrap text-xs md:text-sm text-primary dark:text-custom-white font-medium"
            aria-label={`${reactionsCount} reactions`}
          >
            {reactionsCount} reactions
          </div>
        </div>

        {/* Bookmark */}
        <div
          className="flex items-center space-x-2"
          role="group"
          aria-label="Bookmark and read time"
        >
          {/* Read Time */}
          <div
            className="whitespace-nowrap text-xs md:text-sm text-primary dark:text-custom-white font-medium"
            aria-label={`Estimated read time: ${readTime}`}
          >
            {readTime} read
          </div>

          <Bookmark className="w-5 h-5 dark:text-white" />
        </div>
      </div>

      {/* Posted Time */}
      <div
        className="text-xs text-gray-700 dark:text-secondary"
        aria-label={`Posted ${posted}`}
      >
        Posted {posted}
      </div>
    </div>
  );
}

export default ArticleReactions;
