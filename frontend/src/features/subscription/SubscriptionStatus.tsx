import { useEffect, useState } from 'react';
import Text from '../../components/common/Text';
import Button from '../../components/common/Button';

function SubscriptionStatus() {
  const [isRenewModalOpen, setIsRenewModalOpen] = useState(false);

  useEffect(() => {
    function handleEscapeKey(event: KeyboardEvent) {
      if (event.key === 'Escape') closeRenewModal();
    }

    if (isRenewModalOpen) {
      document.addEventListener('keydown', handleEscapeKey);
    }

    return () => {
      document.removeEventListener('keydown', handleEscapeKey);
    };
  }, [isRenewModalOpen]);
  // TODO: FIX LATER: SO MANY WAYS OF DOING IT

  function openRenewModal() {
    setIsRenewModalOpen(true);
  }

  function closeRenewModal() {
    setIsRenewModalOpen(false);
  }

  return (
    <div className="mb-5 text-gray-900">
      <Text
        variant="h3"
        size="lg"
        bold={false}
        className="dark:text-custom-white font-semibold mb-2"
      >
        Subscription Status
      </Text>
      <div className="border border-gray rounded-lg p-4 dark:text-custom-white">
        <p className="font-semibold">Current Plan</p>
        <p className="text-secondary text-sm mb-1">
          Premium Plan (Expires on 27th January 2026)
        </p>
        <Button type="submit" variant="gradient" onClick={openRenewModal}>
          Renew Subscription
        </Button>
        {/* <Button type="submit" variant="gradient" onClick={openRenewModal}>
          Subscribe to Premium
        </Button> */}
      </div>

      {/* Modal Overlay */}
      {isRenewModalOpen && (
        <div
          className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50"
          onClick={closeRenewModal} // Close modal when clicking outside
          role="dialog"
          aria-modal="true"
          aria-labelledby="modal-title"
        >
          {/* Modal Content */}
          <div
            className="bg-white w-full max-w-md p-6 rounded-lg shadow-lg relative"
            onClick={(e) => e.stopPropagation()} // Prevent closing when clicking inside
          >
            <Text
              variant="h3"
              size="xl"
              bold={false}
              className="font-semibold text-gray-900 mb-4"
            >
              Renew Subscription
            </Text>
            <p className="text-gray-700 mb-6">Select a plan:</p>
            <div className="space-y-4">
              <Button variant="outline">Premium Plan ($1.99/month)</Button>
              <Button variant="outline">Basic Plan (Free)</Button>
              <Button
                variant="primary"
                onClick={closeRenewModal}
                className="block"
              >
                Cancel
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default SubscriptionStatus;
