import { Link } from 'react-router-dom';
import { IoWarning, IoMail, IoCall } from 'react-icons/io5';
import Button from '../../../components/common/Button';

function AccountDisabled() {
  return (
    <div className="flex items-center justify-center pt-22 pb-4">
      <div className="max-w-md w-full p-8 text-center">
        <div className="flex justify-center mb-6">
          <IoWarning className="text-6xl text-red-500" />
        </div>

        <h1 className="text-2xl font-bold text-gray-900 mb-4 dark:text-custom-white">
          Account Disabled
        </h1>

        <p className="text-gray-600 mb-6 dark:text-custom-white">
          Your account has been temporarily disabled. This could be due to:
        </p>

        <ul className="text-left text-gray-600 mb-6 space-y-2 dark:text-custom-white">
          <li>• Violation of our terms of service</li>
          <li>• Suspicious account activity</li>
          <li>• Security concerns</li>
          <li>• Administrative review</li>
        </ul>

        <div className="space-y-3">
          <div className="flex items-center gap-3 text-gray-600 dark:text-custom-white">
            <IoMail className="text-lg text-primary dark:text-custom-white" />
            <span className="text-sm">support@techive.com</span>
          </div>

          <div className="flex items-center gap-3 text-gray-600 dark:text-custom-white">
            <IoCall className="text-lg text-primary dark:text-custom-white" />
            <span className="text-sm">+1 (555) 123-4567</span>
          </div>
        </div>

        <div className="mt-8 space-y-3">
          <Button
            className="w-full"
            onClick={() =>
              (window.location.href =
                'mailto:support@techive.com?subject=Account Disabled - Please Help')
            }
          >
            Contact Support
          </Button>

          <Link to="/login">
            <Button variant="outline" className="w-full">
              Back to Login
            </Button>
          </Link>
        </div>
      </div>
    </div>
  );
}

export default AccountDisabled;
