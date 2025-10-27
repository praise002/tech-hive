import { CiSearch } from 'react-icons/ci';
import { SearchInputProps } from '../../types/types';
import React, { useState } from 'react';

function SearchInput({ inputWidth, iconSize }: SearchInputProps) {
  const [searchValue, setSearchValue] = useState('');

  function handleInputChange(e: React.ChangeEvent<HTMLInputElement>) {
    setSearchValue(e.target.value);
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    console.log('Search query:', searchValue);
  }

  return (
    <form onSubmit={handleSubmit} className="relative">
      {/* Search Icon */}
      <CiSearch
        className={`${iconSize} absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 dark:text-custom-white pointer-events-none`}
        aria-hidden="true"
      />

      {/* Input Field */}
      <input
        className={`${inputWidth} appearance-none dark:text-custom-white border border-gray-500 dark:border-custom-white rounded-md pl-10 pr-3 py-2 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-600 dark:focus-visible:ring-white dark:focus-visible:text-white focus-visible:border-gray-600 dark:focus-visible:border-white`}
        type="search"
        placeholder="Search articles..."
        aria-label="Search articles"
        value={searchValue}
        onChange={handleInputChange}
      />
    </form>
  );
}

export default SearchInput;
