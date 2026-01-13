import { Link } from 'react-router-dom';
import { TagsProps } from '../../types/types';

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
function hashTagName(tagName: string) {
  return tagName
    .toLowerCase()
    .split('')
    .reduce((sum, char) => sum + char.charCodeAt(0), 0);
}

// Map the Hash to a Color
function getTagColor(tagName: string) {
  const hash = hashTagName(tagName);
  return tagColors[hash % tagColors.length];
}

function Tags({ tags }: TagsProps) {
  return (
    <ul className="flex gap-2 flex-wrap my-2 text-xs md:text-sm cursor-pointer">
      {tags.map((tag) => {
        const color = getTagColor(tag.name);
        return (
          <li key={tag.name} className="inline-flex items-center">
            <span className={`text-${color}`} aria-hidden="true">
              #
            </span>
            <Link
              to={`/articles?tag=${encodeURIComponent(tag.name)}`}
              className="dark:text-custom-white"
              aria-label={`Filter articles by tag: ${tag.name}`}
            >
              {tag.name}
            </Link>
          </li>
        );
      })}
    </ul>
  );
}

export default Tags;
