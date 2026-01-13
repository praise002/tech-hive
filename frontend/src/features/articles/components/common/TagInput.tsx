import { useState } from 'react';
import { TagInputProps } from '../../../../types/types';

function TagInput({
  tags,
  suggestedTags,
  value = '',
  onAddTag,
  onInputChange = () => {},
  onInputKeyDown = () => {},
  maxTags = 5,
}: TagInputProps) {
  const [isFocused, setIsFocused] = useState(false); // Tracks whether the input is focused (to show/hide suggestions)

  const filteredSuggestions = value
    ? suggestedTags
        .filter(
          (tag) =>
            tag.toLowerCase().startsWith(value.toLowerCase()) &&
            !tags.includes(tag)
        )
        .slice(0, 5)
    : [];

  return (
    <div className="relative">
      {tags.length < maxTags && (
        <form
          onSubmit={(e) => {
            e.preventDefault();
          }}
        >
          <input
            type="text"
            value={value}
            onChange={onInputChange}
            onKeyDown={onInputKeyDown}
            onFocus={() => setIsFocused(true)}
            onBlur={() => setTimeout(() => setIsFocused(false), 200)}
            placeholder={tags.length === 0 ? 'Add tags...' : 'Add another...'}
            className="w-full p-2 focus:outline-none dark:text-custom-white"
          />
        </form>
      )}

      {/* Suggestions Dropdown */}
      {isFocused && value && filteredSuggestions.length > 0 && (
        <ul className="absolute w-full mt-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 shadow-lg max-h-40 overflow-auto z-10">
          {filteredSuggestions.map((tag) => (
            <li
              key={tag}
              onClick={() => onAddTag(tag)}
              className="px-4 py-2 cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-700"
            >
              {tag}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default TagInput;
