import { Link, NavLink } from 'react-router-dom';
import { useCategories } from '../../hooks/useContent';

function CategoryBar() {
  const { categories, isPending } = useCategories({ page_size: 10 });

  if (isPending) {
    return (
      <nav
        className="lg:flex hidden bg-peach items-center justify-between overflow-x-auto mt-15 px-8 py-4 h-[72px]"
        aria-label="Loading categories"
      >
        <div className="animate-pulse flex space-x-4">
          <div className="h-4 w-24 bg-gray-200 rounded"></div>
          <div className="h-4 w-24 bg-gray-200 rounded"></div>
          <div className="h-4 w-24 bg-gray-200 rounded"></div>
        </div>
      </nav>
    );
  }

  return (
    <nav
      className="lg:flex hidden bg-peach items-center justify-between overflow-x-auto mt-15 px-8 py-4"
      aria-label="Popular tech categories"
    >
      <ul className="flex items-center space-x-6 overflow-x-auto no-scrollbar">
        {categories.map((category) => (
          <li key={category.id} className="whitespace-nowrap">
            <NavLink
              to={`/categories/${category.slug}`}
              className={({ isActive }) =>
                `text-sm font-medium transition-colors hover:text-primary ${
                  isActive ? 'text-primary font-bold' : 'text-gray-700'
                }`
              }
              aria-label={`Browse articles in ${category.name}`}
            >
              {category.name}
            </NavLink>
          </li>
        ))}
      </ul>
      <div className="text-secondary hover:text-red transition-colors whitespace-nowrap ml-4">
        <Link to="/categories" className="text-sm font-semibold">
          See All Categories
        </Link>
      </div>
    </nav>
  );
}

export default CategoryBar;
