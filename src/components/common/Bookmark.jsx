import { FaRegBookmark } from 'react-icons/fa6';
import { FaBookmark } from 'react-icons/fa';
import { useState } from 'react';
import PropTypes from 'prop-types';

function Bookmark( { className= '' }) {
  const [isBookmarked, setIsBookmarked] = useState(false);

  return (
    <>
      {isBookmarked ? (
        <FaBookmark
          className={`cursor-pointer dark:invert ${className}`}
          aria-label="Add bookmark"
          onClick={() => setIsBookmarked(false)}
        />
      ) : (
        <FaRegBookmark
          className={`cursor-pointer dark:invert ${className}`}
          aria-label="Remove bookmark"
          onClick={() => setIsBookmarked(true)}
        />
      )}
    </>
  );
}

Bookmark.propTypes = {
  className: PropTypes.string
};

export default Bookmark;
