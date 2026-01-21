import { useNavigate, useSearchParams } from 'react-router-dom';
import { useVerifyPayment } from '../hooks/useSubscription';
import Spinner from '../../../components/common/Spinner';
import Text from '../../../components/common/Text';
import Button from '../../../components/common/Button';
import { MdCheckCircle, MdError } from 'react-icons/md';

function PaymentStatus() {
  const [searchParams] = useSearchParams();
  const reference = searchParams.get('reference');
  const navigate = useNavigate();

  const { isPending, isError, isSuccess, error } = useVerifyPayment(reference);

  if (!reference) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center p-4">
        <Text variant="h2" size="xl" className="font-bold text-red-500 mb-4">
          Invalid Payment Reference
        </Text>
        <Button onClick={() => navigate('/account')}>Back to Account</Button>
      </div>
    );
  }

  return (
    <div className="min-h-[60vh] flex flex-col items-center justify-center p-4 text-center">
      {isPending && (
        <div className="flex flex-col items-center">
          <Spinner />
          <p className="mt-4 text-gray-600 dark:text-gray-300">
            Verifying your payment...
          </p>
        </div>
      )}

      {isSuccess && (
        <div className="flex flex-col items-center animate-fade-in">
          <MdCheckCircle className="w-20 h-20 text-green-500 mb-4" />
          <Text variant="h2" size="2xl" className="font-bold mb-2">
            Payment Successful!
          </Text>
          <p className="text-gray-600 dark:text-gray-300 mb-8 max-w-md">
            Your subscription has been activated successfully. You now have
            access to all premium features.
          </p>
          <div className="flex gap-4">
            <Button onClick={() => navigate('/account')} variant="gradient">
              Go to Account
            </Button>
            <Button onClick={() => navigate('/')} variant="outline">
              Back Home
            </Button>
          </div>
        </div>
      )}

      {isError && (
        <div className="flex flex-col items-center animate-fade-in">
          <MdError className="w-20 h-20 text-red-500 mb-4" />
          <Text variant="h2" size="2xl" className="font-bold mb-2">
            Payment Verification Failed
          </Text>
          <p className="text-gray-600 dark:text-gray-300 mb-8 max-w-md">
            We couldn't verify your payment. This might be because the
            transaction was cancelled or declined.
            {error && (
              <span className="block mt-2 text-red-400 text-sm">
                Error: {error.message}
              </span>
            )}
          </p>
          <div className="flex gap-4">
            <Button onClick={() => navigate('/account')} variant="primary">
              Try Again
            </Button>
            <Button onClick={() => navigate('/contact')} variant="outline">
              Contact Support
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}

export default PaymentStatus;
