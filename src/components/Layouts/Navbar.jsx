import { useState } from 'react';
import { NavLink } from 'react-router-dom';
import SearchInput from '../common/SearchInput';

function Navbar() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const toggleMenu = () => setIsMenuOpen((prev) => !prev);

  return (
    <nav className="fixed left-0 right-0 top-0 z-50 bg-white shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex justify-between items-center py-3">
        {/* Logo & Nav Links */}

        <div className="flex items-center gap-6">
          <div className="uppercase text-gray-900 text-xl font-bold">
            Tec<span className="text-red-700">Hive.</span>
          </div>
          <div className="hidden lg:flex items-center gap-6 text-gray-900 font-medium">
            <NavLink to="/" className="hover:text-red-700">
              Home
            </NavLink>
            <NavLink to="/categories" className="hover:text-red-700">
              Categories
            </NavLink>
            <NavLink to="/about" className="hover:text-red-700">
              About Us
            </NavLink>
            <NavLink to="/contact" className="hover:text-red-700">
              Contact Us
            </NavLink>
          </div>
        </div>

        {/* Search & Icons */}
        {/* <div className="hidden sm:flex items-center gap-4 text-sm">
          <img
            className="w-6 h-6 text-gray-900"
            src="/src/assets/icons/Vector.png"
            alt="Search Icon"
          />
          <input
            className="border border-gray-500 rounded-md px-3 py-1 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-600 focus-visible:border-gray-600"
            type="search"
            placeholder="Search articles"
          />
        </div> */}

        <div className="hidden lg:flex items-center gap-4 text-sm">
          <img
            className="w-6 h-6 text-gray-900"
            src="/src/assets/icons/Vector.png"
            alt="Search Icon"
          />
          <SearchInput iconSize="text-xl" />
        </div>

        {/* Mobile Menu Toggle */}
        <button onClick={toggleMenu} className="lg:hidden p-2">
          {isMenuOpen ? (
            <svg
              className="w-6 h-6 text-gray-800"
              fill="none"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          ) : (
            <svg
              className="w-6 h-6 text-gray-800"
              fill="none"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M4 6h16M4 12h16m-7 6h7"
              />
            </svg>
          )}
        </button>
      </div>

      {/* Mobile Menu */}
      <ul
        className={`lg:hidden flex-col items-center space-y-4 px-6 pb-6 ${
          isMenuOpen ? 'flex' : 'hidden'
        }`}
      >
        {/* Search & Icons */}
        
        <li className="flex flex-col items-center gap-4 text-xs">
          <img
            className="w-6 h-6 text-gray-900"
            src="/src/assets/icons/Vector.png"
            alt="Search Icon"
          />
          <SearchInput inputWidth="w-40" iconSize="text-xl" />
        </li>
        <li>
          <NavLink to="/" className="block text-gray-800 hover:text-red-700">
            Home
          </NavLink>
        </li>
        <li>
          <NavLink
            to="/categories"
            className="block text-gray-800 hover:text-red-700"
          >
            Categories
          </NavLink>
        </li>
        <li>
          <NavLink
            to="/about"
            className="block text-gray-800 hover:text-red-700"
          >
            About Us
          </NavLink>
        </li>
        <li>
          <NavLink
            to="/contact"
            className="block text-gray-800 hover:text-red-700"
          >
            Contact Us
          </NavLink>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar;
