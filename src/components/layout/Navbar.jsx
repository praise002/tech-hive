import { Link as ScrollLink } from 'react-scroll';
import Logo from './Logo';
import { useState } from 'react';
import { useLocation, Link as RouterLink } from 'react-router-dom';

function Navbar() {
  const [activeSection, setActiveSection] = useState('hero'); // Track active section
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const location = useLocation();

  const toggleMenu = () => setIsMenuOpen((prev) => !prev);

  // Common props for ScrollLink
  const scrollLinkProps = {
    spy: true,
    smooth: true,
    offset: -50,
    duration: 500,
  };

  // Array of menu items
  const menuItems = [
    { id: 'hero', label: 'Home', to: 'hero' },
    { id: 'about', label: 'About', to: 'about' },
    { id: 'causes', label: 'Causes', to: 'causes' },
    { id: 'projects', label: 'Projects', to: 'projects' },
    { id: 'contact', label: 'Contact', to: 'contact' },
    { id: 'donate', label: 'Donate', to: 'donate', isButton: true },
  ];

  return (
    <nav className="fixed left-0 right-0 top-0 z-50 shadow-md bg-white">
      <div className="max-w-full  mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center py-2">
          <div className="flex items-center gap-2">
            <Logo />
            <div>
              {location.pathname === '/' ? (
                // On homepage, use ScrollLink to scroll to the hero section
                <ScrollLink
                  {...scrollLinkProps}
                  activeClass="active"
                  to="hero"
                  onSetActive={() => setActiveSection('hero')}
                  className="cursor-pointer text-lime-500 hover:text-black transition-colors font-bold text-xl tracking-wider"
                >
                  JAFF
                </ScrollLink>
              ) : (
                // On other pages, use RouterLink to navigate to the homepage
                <RouterLink
                  to="/"
                  className="cursor-pointer text-lime-500 hover:text-black transition-colors font-bold text-xl tracking-wider"
                >
                  JAFF
                </RouterLink>
              )}
              <p className="uppercase text-[0.4rem] sm:text-[0.6rem] tracking-wider text-purple-700 font-bold">
                Non-profit organization
              </p>
            </div>
          </div>

          {/* Desktop Menu */}
          <ul className="lg:flex hidden items-center space-x-4">
            {menuItems.map((item) => (
              <li key={item.id}>
                {location.pathname === '/' ? (
                  // On homepage, use ScrollLink to scroll to the section
                  <ScrollLink
                    {...scrollLinkProps}
                    activeClass="active"
                    to={item.to}
                    onSetActive={() => setActiveSection(item.id)}
                    className={
                      item.isButton
                        ? `cursor-pointer text-customGray hover:bg-lime-500 hover:text-white hover:border-lime-500 transition-colors border-2 border-purple-700 rounded-full focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-purple-500 focus-visible:ring-offset-2 px-4 py-2 ${
                            activeSection === item.id ? 'text-lime-500' : ''
                          }`
                        : `cursor-pointer text-customGray hover:text-lime-500 ${
                            activeSection === item.id ? 'text-lime-500' : ''
                          }`
                    }
                  >
                    {item.label}
                  </ScrollLink>
                ) : (
                  // On other pages, use RouterLink to navigate to the homepage
                  <RouterLink
                    to="/"
                    onClick={() => {
                      // Scroll to the section after navigating to the homepage
                      setTimeout(() => {
                        const section = document.getElementById(item.to);
                        if (section) {
                          section.scrollIntoView({ behavior: 'smooth' });
                        }
                      }, 1000);
                    }}
                    className={`cursor-pointer text-customGray hover:text-lime-500 ${
                      activeSection === item.id ? 'text-lime-500' : ''
                    }`}
                  >
                    {item.label}
                  </RouterLink>
                )}
              </li>
            ))}
          </ul>

          {/* Mobile Menu Toggle Button */}
          <button
            onClick={toggleMenu}
            aria-label="Toggle menu"
            className="lg:hidden p-2"
          >
            {isMenuOpen ? (
              <svg
                className="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
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
                className="block lg:hidden"
                width="27"
                height="27"
                fill="currentColor"
                stroke="currentColor"
                strokeWidth="0"
                viewBox="0 0 512 512"
              >
                <path
                  stroke="none"
                  d="M64 384h384v-42.666H64zm0-106.666h384v-42.667H64zM64 128v42.665h384V128z"
                ></path>
              </svg>
            )}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      <ul
        className={`flex-col lg:hidden space-y-4 px-6 pb-8 ${
          isMenuOpen ? 'flex' : 'hidden'
        }`}
      >
        {menuItems.map((item) => (
          <li key={item.id} className={item.isButton ? 'py-2' : ''}>
            {location.pathname === '/' ? (
              // On homepage, use ScrollLink to scroll to the section
              <ScrollLink
                {...scrollLinkProps}
                activeClass="active"
                to={item.to}
                onSetActive={() => setActiveSection(item.id)}
                className={
                  item.isButton
                    ? `cursor-pointer text-customGray hover:bg-lime-500 hover:text-white hover:border-lime-500 transition-colors border-2 border-purple-700 rounded-full focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-purple-500 focus-visible:ring-offset-2 px-4 py-2 ${
                        activeSection === item.id ? 'text-lime-500' : ''
                      }`
                    : `cursor-pointer text-customGray hover:text-lime-500 ${
                        activeSection === item.id ? 'text-lime-500' : ''
                      }`
                }
              >
                {item.label}
              </ScrollLink>
            ) : (
              // On other pages, use RouterLink to navigate to the homepage
              <RouterLink
                to="/"
                onClick={() => {
                  // Scroll to the section after navigating to the homepage
                  setTimeout(() => {
                    const section = document.getElementById(item.to);
                    console.log(section);
                    if (section) {
                      section.scrollIntoView({ behavior: 'smooth' });
                    }
                  }, 1000);
                }}
                className={`cursor-pointer text-customGray hover:text-lime-500 ${
                  activeSection === item.id ? 'text-lime-500' : ''
                }`}
              >
                {item.label}
              </RouterLink>
            )}
          </li>
        ))}
      </ul>
    </nav>
  );
}

export default Navbar;
