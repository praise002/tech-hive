import { FaRegBookmark } from 'react-icons/fa6';
import { FaBookmark } from 'react-icons/fa';
import { useState } from 'react';
import { BookmarkProps } from '../../types/types';

function Bookmark({ className = '' }: BookmarkProps) {
  const [isBookmarked, setIsBookmarked] = useState(false);

  return (
    <span>
      {isBookmarked ? (
        <FaBookmark
          className={`cursor-pointer ${className}`}
          aria-label="Add bookmark"
          onClick={() => setIsBookmarked(false)}
        />
      ) : (
        <FaRegBookmark
          className={`cursor-pointer ${className}`}
          aria-label="Remove bookmark"
          onClick={() => setIsBookmarked(true)}
        />
      )}
    </span>
  );
}

export default Bookmark;
