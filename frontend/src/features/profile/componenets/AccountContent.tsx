import { Link } from 'react-router-dom';
import Button from '../../../components/common/Button';
import Text from '../../../components/common/Text';
import SubscriptionStatus from '../../subscription/SubscriptionStatus';

import LogoutAll from '../../auth/components/LogoutAll';

function AccountContent() {
  

  return (
    <div className="w-full max-w-none space-y-8 min-h-[70vh] lg:grid lg:grid-cols-2 lg:gap-12 lg:space-y-0">
      {/* Profile Management */}
      <div className="dark:text-custom-white text-gray-900">
        <Text
          variant="h3"
          size="lg"
          bold={false}
          className="font-semibold mb-6 dark:text-custom-white"
        >
          Profile Management
        </Text>
        <div className="space-y-4">
          <div className="border border-gray-200 rounded-lg p-8 space-y-6 min-h-[200px] hover:shadow-lg transition-shadow">
            <div>
              <p className="font-semibold mb-3 text-gray-900 dark:text-custom-white text-lg">
                Content & Public Profile
              </p>
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-6 leading-relaxed">
                Manage your public profile and article preferences. Control what
                others see when they visit your profile.
              </p>
            </div>
            <Button variant="outline">
              <Link
                to="/profile"
                className="text-gray-900 dark:text-custom-white"
              >
                View My Profile
              </Link>
            </Button>
          </div>
        </div>
      </div>

      {/* Account Settings */}
      <div className="dark:text-custom-white text-gray-900">
        <Text
          variant="h3"
          size="lg"
          bold={false}
          className="font-semibold mb-6 dark:text-custom-white"
        >
          Account Settings
        </Text>
        <div className="space-y-4">
          <div className="border border-gray-200 rounded-lg p-8 min-h-[200px] hover:shadow-lg transition-shadow">
            <div className="mb-6">
              <p className="font-semibold mb-3 text-gray-900 dark:text-custom-white text-lg">
                Change Password
              </p>
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-6 leading-relaxed">
                Update your password to keep your account secure. Use a strong
                password with a mix of letters, numbers, and symbols.
              </p>
            </div>
            <Button
              variant="outline"
              onClick={() => alert('Redirecting to Change Password')}
            >
              Update Password
            </Button>
          </div>
          <div className="border border-gray-200 rounded-lg p-8 min-h-[200px] hover:shadow-lg transition-shadow">
            <div className="mb-6">
              <p className="font-semibold mb-3 text-gray-900 dark:text-custom-white text-lg">
                Log out of all devices
              </p>
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-6 leading-relaxed">
                Logout across all your device
              </p>
            </div>
            <LogoutAll />
          </div>
        </div>
      </div>

      {/* Subscription Status - Full Width */}
      <SubscriptionStatus />
    </div>
  );
}

export default AccountContent;
