import { Link, NavLink } from 'react-router-dom';

const popularCategories = [
  {
    id: 1,
    name: 'AI & Machine Learning',
    link: 'categories/ai-machine-learning',
  },
  { id: 2, name: 'Blockchain', link: 'categories/blockchain' },
  { id: 3, name: 'Cloud computing', link: 'categories/cloud-computing' },
  { id: 4, name: 'Cybersecurity', link: 'categories/cybersecurity' },
  { id: 5, name: 'Data Science', link: 'categories/data-science' },
  { id: 6, name: 'Web Development', link: 'categories/web-development' },
];

function CategoryBar() {
  return (
    <div className="lg:flex hidden bg-peach items-center justify-between overflow-x-auto mt-15 px-8 py-4">
      <ul className="flex items-center space-x-2 overflow-x-auto ">
        {popularCategories.map((category) => (
          <li key={category.id}>
            <NavLink to={category.link}>{category.name}</NavLink>
          </li>
        ))}
      </ul>
      <div className="text-secondary hover:text-red transition-colors">
        <Link to="categories">See All Categories</Link>
      </div>
    </div>
  );
}

export default CategoryBar;
