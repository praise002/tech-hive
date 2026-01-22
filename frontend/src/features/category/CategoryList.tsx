import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

import Text from '../../components/common/Text';
import Button from '../../components/common/Button';
import Spinner from '../../components/common/Spinner';
import { useCategories } from '../../hooks/useContent';

function CategoryList() {
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const [debouncedSearch, setDebouncedSearch] = useState('');
  const [sort, setSort] = useState('name');

  // Debounce search input
  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedSearch(search);
      setPage(1); // Reset to first page on new search
    }, 500);

    return () => {
      clearTimeout(handler);
    };
  }, [search]);

  const { categories, isPending, isError, error, next, previous, count } =
    useCategories({
      page,
      page_size: 12,
      search: debouncedSearch,
      ordering: sort,
    });
  const totalPages = count ? Math.ceil(count / 12) : 0;

  const options = [
    { value: 'name', name: 'Alphabetical' },
    { value: '-article_count', name: 'Popularity' },
  ];

  return (
    <div className="min-h-screen sm:min-h-0 bg-gray-100 dark:bg-dark mt-10 py-8 px-4 sm:px-6 lg:px-8">
      <div className="">
        <div className="flex items-center justify-between">
          <Text
            variant="h1"
            size="xl"
            className="lg:text-2xl dark:text-custom-white"
          >
            All Categories
          </Text>

          <form>
            <label htmlFor="sort-categories" className="sr-only">
              Sort categories
            </label>
            <select
              id="sort-categories"
              value={sort}
              onChange={(e) => setSort(e.target.value)}
              className="dark:text-custom-white dark:bg-dark py-2 px-4 border border-gray-300 rounded-md focus-visible:outline-none focus:ring-2 focus:ring-gray-700"
            >
              {options.map((option) => (
                <option key={option.name} value={option.value}>
                  {option.name}
                </option>
              ))}
            </select>
          </form>
        </div>

        <label htmlFor="search-categories" className="sr-only">
          Search categories
        </label>
        <input
          id="search-categories"
          type="search"
          placeholder="Search categories..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          aria-label="Search categories"
          className="appearance-none dark:text-custom-white w-full py-2 px-4 mt-4 border border-gray-300 rounded-md focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-red-700"
        />
      </div>

      {isPending ? (
        <div className="min-h-[50vh] flex items-center justify-center">
          <Spinner />
        </div>
      ) : isError ? (
        <div className="min-h-[50vh] flex items-center justify-center">
          <div className="text-center text-red-500">
            Error loading categories: {error?.message}
          </div>
        </div>
      ) : (
        <>
          <div className="max-w-7xl mx-auto grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 mt-8">
            {categories.map((category) => (
              <div
                key={category.id}
                className="bg-white dark:bg-dark-secondary rounded-lg shadow-md p-4 flex flex-col justify-between hover:shadow-lg transition duration-300 border border-gray-200 dark:border-gray-700"
              >
                <Link
                  to={`/categories/${category.slug}`}
                  className="text-lg font-medium text-gray-800 dark:text-custom-white hover:text-red-700"
                  aria-label={`Browse articles in ${category.name}`}
                >
                  {category.name}
                </Link>

                <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
                  {category.desc}
                </p>
              </div>
            ))}
          </div>

          {count > 0 && (
            <nav className="max-w-7xl mx-auto mt-8 flex items-center justify-center">
              <div className="flex items-center space-x-2">
                <Button
                  variant="primary"
                  disabled={!previous}
                  onClick={() => setPage((p) => Math.max(1, p - 1))}
                  aria-label="Go to previous page"
                >
                  Previous
                </Button>

                <span
                  className="text-gray-600 dark:text-gray-400"
                  aria-live="polite"
                >
                  Page {page} of {totalPages}
                </span>
                <Button
                  variant="primary"
                  disabled={!next}
                  onClick={() => setPage((p) => p + 1)}
                  aria-label="Go to next page"
                >
                  Next
                </Button>
              </div>
            </nav>
          )}

          {categories.length === 0 && (
            <div className="text-center py-10 dark:text-custom-white">
              No categories found.
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default CategoryList;
