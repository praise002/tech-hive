import { CiSearch } from 'react-icons/ci';
import { SearchInputProps } from '../../types';

function SearchInput({ inputWidth, iconSize }: SearchInputProps) {
  return (
    <div className="relative">
      {/* Search Icon */}
      <CiSearch
        className={`${iconSize} absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 dark:text-custom-white`}
      />

      {/* Input Field */}
      <input
        className={`${inputWidth} appearance-none dark:text-custom-white border border-gray-500 dark:border-custom-white rounded-md pl-10 pr-3 py-2 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-600 dark:focus-visible:ring-white dark:focus-visible:text-white focus-visible:border-gray-600 dark:focus-visible:border-white`}
        type="search"
        placeholder="Search articles..."
      />
    </div>
  );
}

export default SearchInput;
