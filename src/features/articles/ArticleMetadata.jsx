import { useState } from 'react';
import Button from '../../components/common/Button';
import MarkdownTags from './MarkdownTags';
import TagInput from './TagInput';

const suggestedTags = [
  'JavaScript',
  "Java",
  "Django",
  "Fastapi",
  'React',
  'Node.js',
  'CSS',
  'HTML',
  'TypeScript',
  'Web Development',
  'Database',
  'Cloud',
  'DevOps',
  "Tag 1",
  "Tag 2",
  "Tag 3",
  "Tag 4",
  "Tag 5",
  "Tag 6",
];

function ArticleMetadata() {
  const [tags, setTags] = useState([
    'Cloud Computing',
    'Technology',
    'Innovation',
  ]);
  const [inputValue, setInputValue] = useState('');

  function handleAddTag(tag) {
    if (!tags.includes(tag) && tags.length < 5) {
      setTags((prevTags) => [...prevTags, tag]);
      setInputValue('');
    }
  }

  function handleRemoveTag(tagToRemove) {
    setTags(tags.filter((tag) => tag !== tagToRemove));
  }

  function handleInputChange(e) {
    setInputValue(e.target.value);
  }

  function handleInputKeyDown(e) {
    if (e.key === 'Enter' && inputValue.trim()) {
      e.preventDefault();
      handleAddTag(inputValue.trim());
    } else if (e.key === 'Backspace' && !inputValue && tags.length > 0) {
      handleRemoveTag(tags[tags.length - 1]);
    }
  }

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
        <MarkdownTags tags={tags} onRemove={handleRemoveTag} />
        <TagInput
          tags={tags}
          onAddTag={handleAddTag}
          suggestedTags={suggestedTags}
          value={inputValue}
          onInputChange={handleInputChange}
          onInputKeyDown={handleInputKeyDown}
        />
      </div>
    </div>
  );
}

export default ArticleMetadata;
