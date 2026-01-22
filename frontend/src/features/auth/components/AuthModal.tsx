import { Link } from 'react-router-dom';
import { useAuthModal } from '../../../context/AuthModalContext';
import Button from '../../../components/common/Button';
import Text from '../../../components/common/Text';
import { XMarkIcon } from '@heroicons/react/24/outline';

const AuthModal = () => {
  const { isAuthModalOpen, closeAuthModal } = useAuthModal();

  if (!isAuthModalOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 overflow-y-auto overflow-x-hidden bg-black/50 backdrop-blur-sm">
      <div className="relative w-full max-w-md max-h-full rounded-2xl bg-white p-6 shadow-2xl dark:bg-gray-800">
        {/* Close Button */}
        <button
          onClick={closeAuthModal}
          type="button"
          className="absolute top-4 right-4 text-gray-400 hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-gray-300 rounded-lg text-sm w-8 h-8 inline-flex justify-center items-center dark:hover:text-white"
          aria-label="Close modal"
        >
          <XMarkIcon className="w-5 h-5" />
        </button>

        <div className="text-center">
          {/* Illustration or Icon could go here */}
          <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-peach/20 dark:bg-peach/10">
            <svg
              className="h-8 w-8 text-peach"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"
              ></path>
            </svg>
          </div>

          <Text variant="h3" className="mb-2 text-gray-900 dark:text-white">
            Join the Community
          </Text>

          <Text className="mb-8 text-gray-500 dark:text-gray-400">
            Log in or sign up to like posts, reply to comments, and join the
            discussion on Tech Hive.
          </Text>

          <div className="flex flex-col space-y-3">
            <Button onClick={closeAuthModal} className="w-full">
              <Link to="/register" className="block w-full h-full">
                Sign Up
              </Link>
            </Button>

            <Button
              variant="outline"
              onClick={closeAuthModal}
              className="w-full"
            >
              <Link to="/login" className="block w-full h-full">
                Log In
              </Link>
            </Button>
          </div>

          <div className="mt-6 text-sm text-gray-500 dark:text-gray-400">
            Maybe later?{' '}
            <button
              onClick={closeAuthModal}
              className="font-medium text-peach hover:underline text-sm ml-1"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AuthModal;
