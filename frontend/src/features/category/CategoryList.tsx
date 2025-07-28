import { Link } from 'react-router-dom';

import Text from '../../components/common/Text';
import Button from '../../components/common/Button';

const allCategories = [
  {
    id: 1,
    name: 'AI & Machine Learning',
    link: '/categories/ai-machine-learning',
    description: 'Explore articles and resources on AI and machine learning.',
  },
  {
    id: 2,
    name: 'Blockchain',
    link: '/categories/blockchain',
    description: 'Learn about blockchain technology and its applications.',
  },
  {
    id: 3,
    name: 'Cloud Computing',
    link: '/categories/cloud-computing',
    description: 'Dive into cloud computing trends and tools.',
  },
  {
    id: 4,
    name: 'Cybersecurity',
    link: '/categories/cybersecurity',
    description: 'Stay updated on cybersecurity best practices.',
  },
  {
    id: 5,
    name: 'Data Science',
    link: '/categories/data-science',
    description: 'Discover data science techniques and tools.',
  },
  {
    id: 6,
    name: 'Web Development',
    link: '/categories/web-development',
    description: 'Enhance your web development skills with our resources.',
  },
  // Add more categories as needed
];

function CategoryList() {
  const options = [
    {
      value: '',
      name: 'Sort by',
    },
    {
      value: 'alphabetical',
      name: 'Alphabetical',
    },
    {
      value: 'popularity',
      name: 'Popularity',
    },
  ];

  return (
    <div className="min-h-screen sm:min-h-0 bg-gray-100 dark:bg-dark mt-10 py-8 px-4 sm:px-6 lg:px-8">
      {/* Sticky Search Bar */}
      <div className="">
        {/* Page Title */}
        <div className="flex items-center justify-between">
          <Text
            variant="h1"
            size="xl"
            className="lg:text-2xl dark:text-custom-white"
          >
            All Categories
          </Text>

          {/* Sorting Dropdown (Static) */}
          <form>
            <label htmlFor="sort-categories" className="sr-only">
              Sort categories
            </label>
            <select
              id="sort-categories"
              className="dark:text-custom-white dark:bg-dark py-2 px-4 border border-gray-300 rounded-md focus-visible:outline-none focus-visible:ring-2 focus:ring-gray-700"
            >
              {options.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.name}
                </option>
              ))}
            </select>
          </form>
        </div>
        {/* Search Bar */}
        <label htmlFor="search-categories" className="sr-only">
          Search categories
        </label>
        <input
          id="search-categories"
          type="search"
          placeholder="Search categories..."
          aria-label="Search categories"
          className="appearance-none dark:text-custom-white w-full py-2 px-4 mt-4 border border-gray-300 rounded-md focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-red-700"
        />
      </div>

      {/* Category Grid */}
      <div className="max-w-7xl mx-auto grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 mt-8">
        {allCategories.map((category) => (
          <div
            key={category.id}
            className="bg-white rounded-lg shadow-md p-4 flex flex-col justify-between hover:shadow-lg transition duration-300"
          >
            <Link
              to={category.link}
              className="text-lg font-medium text-gray-800 hover:text-red-700"
              aria-label={`Browse articles in ${category.name}`}
            >
              {category.name}
            </Link>

            {/* Category Description */}
            <p className="mt-2 text-sm text-gray-600">{category.description}</p>
          </div>
        ))}
      </div>
      {/* Static Pagination */}
      <nav className="max-w-7xl mx-auto mt-8 flex items-center justify-center">
        <div className="flex items-center space-x-2">
          <Button variant="primary" aria-label="Go to previous page">Previous</Button>

          <span className="text-gray-600" aria-live="polite">Page 1 of 5</span>
          <Button variant="primary" aria-label="Go to next page">Next</Button>
        </div>
      </nav>
    </div>
  );
}

export default CategoryList;
// ADD SORTING, PAGINATION
