import { useState } from 'react';
import Button from '../../components/common/Button';
import MarkdownTags from './MarkdownTags';
import TagInput from './TagInput';
import toast from 'react-hot-toast';
import Spinner from '../../components/common/Spinner';
import { ToolTip } from '../../components/common/SocialLinks';
import Text from '../../components/common/Text';

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

function ArticleMetadata({ mode }: { mode: string }) {
  const [tags, setTags] = useState([
    'Cloud Computing',
    'Technology',
    'Innovation',
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isImageLoading, setIsImageLoading] = useState(false);

  const [metadata, setMetadata] = useState({
    title: 'Test Title',
    // coverImage: '/assets/about.png',
    coverImage: '',
    coverImageAlt: '',
  });

  const [isAltTextModalOpen, setIsAltTextModalOpen] = useState(false);
  const [altTextInput, setAltTextInput] = useState('');
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false);

  function handleAltTextInputChange(e: React.ChangeEvent<HTMLInputElement>) {
    setAltTextInput(e.target.value);
    setHasUnsavedChanges(e.target.value !== metadata.coverImageAlt);
  }

  function handleSaveAltText() {
    setMetadata((prev) => ({
      ...prev,
      coverImageAlt: altTextInput,
    }));
    setHasUnsavedChanges(false);
    setIsAltTextModalOpen(false);
  }

  function handleOpenAltTextModal() {
    setAltTextInput(metadata.coverImageAlt);
    setHasUnsavedChanges(false);
    setIsAltTextModalOpen(true);
  }

  function handleCloseAltTextModal() {
    if (hasUnsavedChanges) {
      const shouldDiscard = window.confirm(
        'You have unsaved changes. Do you want to discard them?'
      );
      if (!shouldDiscard) return;
    }

    setIsAltTextModalOpen(false);
    setAltTextInput('');
    setHasUnsavedChanges(false);
  }

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
    <div className={`${mode === 'edit' ? 'mb-8' : 'mb-2'} mt-2`}>
      {/* Cover Image Section */}

      {mode === 'edit' && (
        <div className="mb-6 relative">
          {metadata.coverImage ? (
            <div className="relative group">
              <img
                src={metadata.coverImage}
                alt={metadata.coverImageAlt || 'Cover Image'}
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
                  <button
                    type="button"
                    onClick={handleOpenAltTextModal}
                    className="bg-white relative text-gray-800 px-4 py-2 rounded-md"
                  >
                    {metadata.coverImageAlt ? 'Edit Alt Text' : 'Add Alt Text'}
                  </button>
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
      )}

      {/* Modal Overlay */}
      {isAltTextModalOpen && (
        <div
          className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50"
          onClick={handleCloseAltTextModal} // Close modal when clicking outside
          role="dialog"
          aria-modal="true"
          aria-labelledby="modal-title"
        >
          {/* Modal Content */}
          <div
            className="bg-white w-full max-w-xl p-6 rounded-lg shadow-lg relative"
            onClick={(e) => e.stopPropagation()} // Prevent closing when clicking inside
          >
            <Text
              variant="h3"
              size="xl"
              bold={false}
              className="font-semibold text-gray-900 mb-4"
            >
              Alternative text
            </Text>
            <p className="text-gray-700 mb-6">
              Write a brief description of this image for readers with visual
              impairments
            </p>

            <input
              type="text"
              value={altTextInput}
              onChange={handleAltTextInputChange}
              placeholder="Example: A cat sitting on a couch"
              className="appearance-none block w-full px-4 py-2 border border-gray-300 rounded-md focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-800 focus-visible:border-gray-800"
            />

            <div className="space-x-4 mt-4">
              <Button variant="outline" onClick={handleSaveAltText}>
                Save
              </Button>
              <Button onClick={handleCloseAltTextModal}>
                {hasUnsavedChanges ? 'Discard' : 'Cancel'}
              </Button>
            </div>
          </div>
        </div>
      )}

      {mode === 'preview' && metadata.coverImage && (
        <img
          src={metadata.coverImage}
          alt="Cover Image"
          className="w-full h-64 sm:h-80 object-cover rounded-lg"
        />
      )}

      {/* Title Section */}
      {mode === 'edit' ? (
        <div className="mb-6">
          <input
            type="text"
            placeholder="Enter your new post title..."
            value={metadata.title}
            onChange={handleTitleChange}
            className="w-full text-3xl sm:text-4xl font-bold border-0 focus:ring-0 focus:outline-none placeholder-gray-400 dark:placeholder-gray-500 text-gray-900 dark:text-custom-white"
          />
        </div>
      ) : (
        <Text
          variant="h1"
          size="lg"
          bold={false}
          className="font-semibold my-2 text-gray-900 dark:text-custom-white"
        >
          {metadata.title}
        </Text>
      )}

      {/* Tags Section */}
      <>
        {mode === 'edit' ? (
          <div className="flex items-center gap-2 flex-wrap my-2 text-xs md:text-sm">
            <MarkdownTags tags={tags} mode="edit" onRemove={handleRemoveTag} />
            <TagInput
              tags={tags}
              onAddTag={handleAddTag}
              suggestedTags={suggestedTags}
              value={inputValue}
              onInputChange={handleInputChange}
              onInputKeyDown={handleInputKeyDown}
            />
          </div>
        ) : (
          <div className="flex items-center gap-2 flex-wrap my-2 text-xs md:text-sm">
            <MarkdownTags tags={tags} mode="preview" onRemove={() => {}} />
          </div>
        )}
      </>
    </div>
  );
}

export default ArticleMetadata;
