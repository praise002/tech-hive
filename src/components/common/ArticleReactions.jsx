import PropTypes from 'prop-types';

function ArticleReactions({ reactions, reactionsCount, posted, readTime }) {
  return (
    <div className="flex flex-col">
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
              >
                {reaction}
              </span>
            ))}
          </div>
          <div className="whitespace-nowrap text-sm text-color-text-primary font-medium">
            {reactionsCount} reactions
          </div>
        </div>

        {/* Bookmark */}
        <div className="flex items-center space-x-2">
          {/* Read Time */}
          <div className="whitespace-nowrap text-sm text-color-text-primary  font-medium">
            {readTime} read
          </div>
          <img
            src="/src/assets/icons/bookmark-light.png"
            alt="Bookmark"
            className="w-5 h-5"
          />
        </div>
      </div>

      {/* Posted Time */}
      <div className="text-xs text-color-text-secondary">Posted {posted}</div>
    </div>
  );
}

ArticleReactions.propTypes = {
  reactions: PropTypes.arrayOf(PropTypes.string).isRequired,
  reactionsCount: PropTypes.number.isRequired,
  posted: PropTypes.string.isRequired,
  readTime: PropTypes.string.isRequired,
};

export default ArticleReactions;
