import { useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { useUnsubscribeNewsletter } from '../hooks/useGeneral';
import Button from '../components/common/Button';
import Spinner from '../components/common/Spinner';
import { MdCheckCircle, MdError } from 'react-icons/md';

const Unsubscribe = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const token = searchParams.get('token');

  const { unsubscribeNewsletter, isPending, isSuccess, isError, error } =
    useUnsubscribeNewsletter();

  useEffect(() => {
    if (token) {
      unsubscribeNewsletter(token);
    }
  }, [token, unsubscribeNewsletter]);

  return (
    <div className="py-20 min-h-[60vh] flex items-center justify-center">
      <div className="container mx-auto px-4 max-w-md text-center">
        <div className="bg-white dark:bg-dark-light p-8 rounded-2xl shadow-lg border border-gray-100 dark:border-gray-800">
          {!token ? (
            <div className="space-y-4">
              <MdError className="w-16 h-16 mx-auto text-red-500" />
              <h1 className="text-2xl font-bold font-heading">Invalid Link</h1>
              <p className="text-gray-600 dark:text-gray-400">
                The unsubscribe link is invalid.
              </p>
              <Button onClick={() => navigate('/')} variant="primary">
                Go Home
              </Button>
            </div>
          ) : isPending ? (
            <div className="space-y-4">
              <div className="flex justify-center">
                <Spinner />
              </div>
              <p className="text-lg font-medium animate-pulse">
                Unsubscribing you...
              </p>
            </div>
          ) : isSuccess ? (
            <div className="space-y-6">
              <MdCheckCircle className="w-20 h-20 mx-auto text-green-500" />
              <div>
                <h1 className="text-2xl font-bold font-heading mb-2">
                  Unsubscribed
                </h1>
                <p className="text-gray-600 dark:text-gray-400">
                  You have been successfully unsubscribed from our newsletter.
                  We're sorry to see you go!
                </p>
              </div>
              <Button
                onClick={() => navigate('/')}
                variant="primary"
                className="w-full"
              >
                Return to Home
              </Button>
            </div>
          ) : isError ? (
            <div className="space-y-4">
              <MdError className="w-16 h-16 mx-auto text-red-500" />
              <h1 className="text-2xl font-bold font-heading">Error</h1>
              <p className="text-gray-600 dark:text-gray-400">
                {error?.message || 'Something went wrong while unsubscribing.'}
              </p>
              <Button onClick={() => navigate('/')} variant="outline">
                Go Home
              </Button>
            </div>
          ) : null}
        </div>
      </div>
    </div>
  );
};

export default Unsubscribe;
