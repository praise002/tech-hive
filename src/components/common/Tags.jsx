import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';

// Define a Color Palette
const tagColors = [
  'purple-600', // Purple
  'orange-500', // Orange
  'pink-600', // Pink
  'blue-500', // Blue
  'green-500', // Green
  'red-500', // Red
];

// Create a Hashing Function
function hashTagName(tagName) {
  const stringTagName = String(tagName);
  return stringTagName
    .toLowerCase()
    .split('')
    .reduce((sum, char) => sum + char.charCodeAt(0), 0);
}

// Map the Hash to a Color
function getTagColor(tagName) {
  const hash = hashTagName(tagName);
  return tagColors[hash % tagColors.length];
}

function Tags({ tags }) {
  return (
    <div className="flex gap-2 flex-wrap my-2 text-xs md:text-sm">
      {tags.map((tag) => {
        const color = getTagColor(tag);
        return (
          <div
            key={tag}
            className="inline-flex items-center"
          >
            <span className={`text-${color}`}>#</span>
            <button type="button" className="dark:text-custom-white">
              <Link to={`/${tag}`}>{tag}</Link>
            </button>
          </div>
        );
      })}
    </div>
  );
}

Tags.propTypes = {
  tags: PropTypes.arrayOf(PropTypes.string).isRequired,
};

export default Tags;
