import { MdOutlineLightMode, MdOutlineDarkMode } from 'react-icons/md';
import { useContext, useState } from 'react';
import { NavLink } from 'react-router-dom';
import SearchInput from '../common/SearchInput';
import { ThemeContext } from '../../context/ThemeContext';
import { IoMdNotificationsOutline } from 'react-icons/io';

function Navbar() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const toggleMenu = () => setIsMenuOpen((prev) => !prev);

  // Use the ThemeContext
  const { theme, toggleTheme } = useContext(ThemeContext);

  const navLinks = [
    { to: '/', name: 'Home' },
    { to: 'categories', name: 'Categories' },
    { to: 'about', name: 'About Us' },
    { to: 'contact', name: 'Contact Us' },
    // { to: 'account', name: 'Profile' },
    // {to: "dashboard", name: "Dashboard"},
  ];

  return (
    <nav
      className="fixed left-0 right-0 top-0 z-50 bg-white shadow-md dark:bg-dark"
      role="navigation"
      aria-label="Main navigation"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex justify-between items-center py-3">
        {/* Logo & Nav Links */}

        <div className="flex items-center gap-6">
          <div className="uppercase text-gray-900 dark:text-custom-white text-xl font-bold">
            Tec<span className="text-red-600">Hive.</span>
          </div>
          <ul className="hidden lg:flex items-center gap-6 text-gray-900 dark:text-custom-white font-medium">
            {navLinks.map(({ to, name }) => (
              <li key={to}>
                <NavLink to={to} className="hover:text-red-600">
                  {name}
                </NavLink>
              </li>
            ))}
          </ul>
        </div>

        {/* Search & Icons */}
        <div className="hidden lg:flex items-center gap-4 text-sm">
          {/* Theme Toggle Button */}
          <button
            aria-label="Notifications, you have 2 unread notifications"
            type="button"
            onClick={toggleTheme}
          >
            {theme === 'light' ? (
              <MdOutlineDarkMode
                className="w-6 h-6 text-gray-900 dark:text-white"
                aria-hidden="true"
              />
            ) : (
              <MdOutlineLightMode
                className="w-6 h-6 text-gray-900 dark:text-white"
                aria-hidden="true"
              />
            )}
          </button>

          <SearchInput iconSize="text-xl" />
        </div>

        <div className="lg:flex items-center gap-6 hidden">
          <button
            className="relative"
            aria-label="Notifications, you have 2 unread notifications"
            type="button"
          >
            <div
              aria-hidden="true"
              className="absolute right-0 rounded-full bg-red w-5 h-5 flex items-center justify-center"
            >
              <span className="text-white text-xs">2</span>
              {/* FIXME: IT BREAKS AT 3 DIGIT NUMBER */}
            </div>
            <IoMdNotificationsOutline
              className="w-10 h-10 text-gray-900 dark:text-white"
              aria-hidden="true"
            />
          </button>

          <div>
            <img
              className="w-10 h-10 rounded-full object-cover"
              src="/assets/icons/Avatars.png"
              alt="Profile Picture"
            />
          </div>
        </div>

        {/* Mobile Menu Toggle */}
        <button
          aria-label={`${isMenuOpen ? 'Close' : 'Open'} navigation menu`}
          onClick={toggleMenu}
          type="button"
          aria-expanded={isMenuOpen}
          aria-controls="mobile-menu"
          className="lg:hidden p-2"
        >
          {isMenuOpen ? (
            <svg
              className="w-6 h-6 text-gray-800 dark:text-custom-white"
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
              className="w-6 h-6 text-gray-800 dark:text-custom-white"
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
        role="menu"
        aria-labelledby="mobile-menu-button"
      >
        {/* Search & Icons */}

        <li className="flex flex-col items-center gap-4 text-xs">
          {/* Theme Toggle Button */}
          <button
            aria-label={`Switch to ${
              theme === 'light' ? 'dark' : 'light'
            } mode`}
            type="button"
            onClick={toggleTheme}
          >
            {theme === 'light' ? (
              <MdOutlineDarkMode className="w-6 h-6 text-gray-900 dark:text-white" />
            ) : (
              <MdOutlineLightMode className="w-6 h-6 text-gray-900 dark:text-white" />
            )}
          </button>

          <SearchInput inputWidth="w-40" iconSize="text-xl" />
        </li>
        {navLinks.map((nav) => (
          <li key={nav.to}>
            <NavLink
              to={nav.to}
              className="block text-gray-800 dark:text-custom-white hover:text-red-700"
            >
              {nav.name}
            </NavLink>
          </li>
        ))}

        {/* Profile Picture */}
        <li className="flex items-center space-x-2">
          <button
            type="button"
            className="relative"
            aria-label="Notifications, you have 2 unread notifications"
          >
            <div
              aria-hidden="true"
              className="absolute right-0 rounded-full bg-red w-4 h-4 flex items-center justify-center"
            >
              <span className="text-white text-xs">2</span>
              {/* FIXME: IT BREAKS AT 3 DIGIT NUMBER */}
            </div>
            <IoMdNotificationsOutline
              aria-hidden="true"
              className="w-8 h-8 text-gray-900 dark:text-white"
            />
          </button>
          <img
            className="w-8 h-8 rounded-full object-cover"
            src="/assets/icons/Avatars.png"
            alt="Profile Picture"
          />
          <span className="font-medium text-gray-800 dark:text-custom-white">
            Elizabeth Stone
          </span>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar;
