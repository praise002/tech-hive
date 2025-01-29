import PropTypes from 'prop-types';
import { CiSearch } from 'react-icons/ci';

function SearchInput({ inputWidth, iconSize }) {
  return (
    <div className="relative">
      {/* Search Icon */}
      <CiSearch className={`${iconSize} absolute left-3 top-1/2 -translate-y-1/2 text-gray-500`} />

      {/* Input Field */}
      <input
        className={`${inputWidth} border border-gray-500 rounded-md pl-10 pr-3 py-2 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-600 focus-visible:border-gray-600`}
        type="search"
        placeholder="Search articles..."
      />
    </div>
  );
}

// ✅ Props Validation
SearchInput.propTypes = {
  inputWidth: PropTypes.string,
  iconSize: PropTypes.string,
};

export default SearchInput;
