import PropTypes from 'prop-types';

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

function MarkdownTags({ tags }) {
  return (
    <div className="flex gap-2 flex-wrap my-2 text-xs md:text-sm">
      {tags.map((tag) => {
        const color = getTagColor(tag);
        return (
          <div key={tag} className="inline-flex items-center px-3 py-1 rounded-lg text-sm font-medium bg-gray-200 text-gray-800 dark:bg-gray-700 dark:text-gray-200">
            <span className={`text-${color}`}>#</span>
            <button type="button" className="dark:text-custom-white ml-1.5">
              {tag}
            </button>
            <button className="cursor-pointer ml-1.5 text-gray-500 text-2xl hover:text-red dark:text-gray-400">
              &times;
            </button>
          </div>
        );
      })}
    </div>
  );
}

MarkdownTags.propTypes = {
  tags: PropTypes.arrayOf(PropTypes.string).isRequired,
};

export default MarkdownTags;
