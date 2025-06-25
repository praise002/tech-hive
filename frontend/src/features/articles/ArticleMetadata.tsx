import { useState } from 'react';
import Button from '../../components/common/Button';
import MarkdownTags from './MarkdownTags';
import TagInput from './TagInput';
import toast from 'react-hot-toast';
import Spinner from '../../components/common/Spinner';
import { ToolTip } from '../../components/common/SocialLinks';

const suggestedTags = [
  'JavaScript',
  'Java',
  'Django',
  'Fastapi',
  'React',
  'Node.js',
  'CSS',
  'HTML',
  'TypeScript',
  'Web Development',
  'Database',
  'Cloud',
  'DevOps',
  'Tag 1',
  'Tag 2',
  'Tag 3',
  'Tag 4',
  'Tag 5',
  'Tag 6',
];

function ArticleMetadata() {
  const [tags, setTags] = useState([
    'Cloud Computing',
    'Technology',
    'Innovation',
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isImageLoading, setIsImageLoading] = useState(false);

  const [metadata, setMetadata] = useState({
    title: 'Test Title',
    // coverImage: '/src/assets/about.png',
    coverImage: '',
  });

  function handleCoverImageChange(event: React.ChangeEvent<HTMLInputElement>) {
    setIsImageLoading(true);
    const file = event.target.files?.[0];
    if (file) {
      const imageUrl = URL.createObjectURL(file);
      setTimeout(() => {
        setMetadata((prev) => ({
          ...prev,
          coverImage: imageUrl,
        }));
        setIsImageLoading(false);
      }, 900);
    }

    toast.success('Cover picture updated successfully!');
  }

  function handleCoverImageRemove() {
    setMetadata((prev) => ({
      ...prev,
      coverImage: '',
    }));
  }

  function handleTitleChange(e: React.ChangeEvent<HTMLInputElement>) {
    setMetadata((prev) => ({
      ...prev,
      title: e.target.value,
    }));
  }

  function handleAddTag(tag: string) {
    if (!tags.includes(tag) && tags.length < 5) {
      setTags((prevTags) => [...prevTags, tag]);
      setInputValue('');
    }
  }

  function handleRemoveTag(tagToRemove: string) {
    setTags(tags.filter((tag) => tag !== tagToRemove));
  }

  function handleInputChange(e: React.ChangeEvent<HTMLInputElement>) {
    setInputValue(e.target.value);
  }

  function handleInputKeyDown(e: React.KeyboardEvent<HTMLInputElement>) {
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
        {metadata.coverImage ? (
          <div className="relative group">
            <img
              src={metadata.coverImage}
              alt="Cover Image"
              className="w-full h-64 sm:h-80 object-cover rounded-lg"
            />
            <div className="absolute inset-0 group-hover:bg-opacity-30 transition-all duration-300 flex justify-center items-center">
              <div className="space-x-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                <button
                  disabled={isImageLoading}
                  className={`bg-white relative text-gray-800 px-4 py-2 rounded-md ${
                    isImageLoading
                      ? 'cursor-not-allowed opacity-75'
                      : 'cursor-pointer'
                  }`}
                >
                  <input
                    type="file"
                    accept="image/*"
                    className="appearance-none opacity-0 absolute inset-0"
                    onChange={handleCoverImageChange}
                  />
                  {isImageLoading ? <Spinner /> : 'Change'}
                </button>
                <Button onClick={handleCoverImageRemove}>Remove</Button>
              </div>
            </div>
          </div>
        ) : (
          <ToolTip
            position="bottom"
            text="Use a ratio of 1000:420 for best results"
          >
            <Button
              className={`${
                isImageLoading
                  ? 'cursor-not-allowed opacity-75'
                  : 'cursor-pointer'
              }`}
              disabled={isImageLoading}
              variant="outline"
            >
              {/* accept=".jpg, .jpeg, .png, .gif, .webp" */}
              <input
                type="file"
                accept="image/*"
                className="appearance-none absolute inset-0 opacity-0"
                onChange={handleCoverImageChange}
              />
              {isImageLoading ? <Spinner /> : 'Add a cover image'}
            </Button>
          </ToolTip>
        )}
      </div>
      {/* Title Section */}
      <div className="mb-6">
        <input
          type="text"
          placeholder="Enter your new post title..."
          value={metadata.title}
          onChange={handleTitleChange}
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
