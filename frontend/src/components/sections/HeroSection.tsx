import { Link } from 'react-router-dom';
import { Link as ScrollLink } from 'react-scroll';
import Button from '../common/Button';
import Text from '../common/Text';
import Logout from '../../features/auth/components/Logout';
import { useUser } from '../../features/profile/hooks/useUser';

function HeroSection() {
  const { isAuthenticated } = useUser();

  return (
    <section className="relative mt-12 dark:bg-light bg-gradient-to-r from-coral/50 to-peach py-10 px-7 sm:py-20 sm:px-14 overflow-hidden">
      {/* ✅ SVG Background */}
      <img
        src="/assets/hero-section.svg"
        alt=""
        className="pointer-events-none absolute inset-0 w-full h-full object-cover opacity-70"
        aria-hidden="true"
      />

      {/* ✅ Text and Buttons */}
      <Text variant="h2" size="2xl" align="center" className="sm:text-3xl mb-8">
        Your Gateway to the Latest in <br /> Tech Innovation
      </Text>

      <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-4 mb-8">
        {isAuthenticated ? (
          <Logout />
        ) : (
          <Button variant="outline">
            <Link to="/login" aria-label="Login to your account">
              Login
            </Link>
          </Button>
        )}

        {/* TODO: LATER CHECK IF NOT A CONTRIBUTOR */}
        {isAuthenticated ? (
          <Button>
            <Link to="/" aria-label="Register a new account">
              Contribute to Tech Hive
            </Link>
          </Button>
        ) : (
          <Button>
            <Link to="/register" aria-label="Register a new account">
              Register
            </Link>
          </Button>
        )}
      </div>

      <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-4">
        <span className="italic text-gray-800">Never miss an update!</span>

        <Button variant="gradient">
          <ScrollLink to="subscribe" smooth={true} duration={500}>
            Subscribe to newsletter
          </ScrollLink>
        </Button>
      </div>
    </section>
  );
}

export default HeroSection;
