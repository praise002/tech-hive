import Button from '../../components/common/Button';
import MarkdownTags from './MarkdownTags';

const tags = ['Cloud Computing', 'Technology', 'Innovation'];
const suggestedTags = [
  'JavaScript',
  'React',
  'Node.js',
  'CSS',
  'HTML',
  'TypeScript',
  'Web Development',
  'Database',
  'Cloud',
  'DevOps',
];

function ArticleMetadata() {
  return (
    <div className="mb-8 mt-2">
      {/* Cover Image Section */}
      <div className="mb-6 relative">
        <Button variant="outline">
          {/* accept=".jpg, .jpeg, .png, .gif, .webp" */}
          <input type="file" accept="image/*" className="hidden" />
          Add a cover image
        </Button>
      </div>
      {/* Title Section */}
      <div className="mb-6">
        <input
          type="text"
          placeholder="Enter your new post title..."
          className="w-full text-3xl sm:text-4xl font-bold border-0 focus:ring-0 focus:outline-none placeholder-gray-400 dark:placeholder-gray-500 text-gray-900 dark:text-custom-white"
        />
      </div>
      {/* Tags Section */}
      <div className="mb-6 flex items-center">
        <MarkdownTags tags={tags} />
        <div className="relative flex-1">
          <input
            type="text"
            list="tag-suggestions"
            placeholder="Add tags..."
            className="w-full p-2 focus:outline-none dark:text-custom-white"
          />
          {/* Add another */}
          <datalist id="tag-suggestions">
            {suggestedTags.map((tag) => (
              // <option key={tag} value={tag}>
              //   {tag}
              // </option>
              <option key={tag} value={tag} />
            ))}
          </datalist>
        </div>
      </div>
    </div>
  );
}

export default ArticleMetadata;
