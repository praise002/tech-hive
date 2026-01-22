import { useEffect, useState } from 'react';
import Text from '../../components/common/Text';
import Button from '../../components/common/Button';
import {
  useMySubscription,
  usePlans,
  useSubscribe,
} from './hooks/useSubscription';
import { formatDate } from '../../utils/utils';
import Spinner from '../../components/common/Spinner';
import { SubscriptionPlan } from '../../types/subscription';

function SubscriptionStatus() {
  const [isRenewModalOpen, setIsRenewModalOpen] = useState(false);
  const { subscription, isPending, isError } = useMySubscription();
  const { plans, isPending: isPlansPending } = usePlans();
  const { subscribe, isPending: isSubscribing } = useSubscribe();

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

  function openRenewModal() {
    setIsRenewModalOpen(true);
  }

  function closeRenewModal() {
    setIsRenewModalOpen(false);
  }

  const handleSubscribe = (planId: string) => {
    subscribe(
      { plan_id: planId, start_trial: false },
      {
        onSuccess: (data) => {
          if (data.authorization_url) {
            window.location.href = data.authorization_url;
          }
        },
      }
    );
  };

  if (isPending) return <Spinner />;

  // Default to showing "Free Plan" if no subscription or error (assuming backend 404 means no active sub)
  const isPremium = subscription?.is_premium;
  const planName = subscription?.plan?.name || 'Free Plan';
  const expiryDate = subscription?.current_period_end;

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
          {planName} {expiryDate && `(Expires on ${formatDate(expiryDate)})`}
        </p>

        {!isPremium && (
          <Button
            type="button"
            variant="gradient"
            onClick={openRenewModal}
            disabled={isSubscribing}
          >
            Upgrade to Premium
          </Button>
        )}

        {isPremium && (
          <Button
            type="button"
            variant="outline"
            onClick={openRenewModal} // Or handle Manage Subscription
          >
            Manage Subscription
          </Button>
        )}
      </div>

      {/* Modal Overlay */}
      {isRenewModalOpen && (
        <div
          className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50 text-gray-900"
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
              {isPremium ? 'Manage Subscription' : 'Upgrade Plan'}
            </Text>

            {isPlansPending ? (
              <Spinner />
            ) : (
              <>
                <p className="text-gray-700 mb-6">Select a plan:</p>
                <div className="space-y-4">
                  {plans?.map((plan: SubscriptionPlan) => (
                    <div key={plan.id} className="flex flex-col gap-2">
                      <Button
                        variant="outline"
                        onClick={() => handleSubscribe(plan.id)}
                        disabled={
                          isSubscribing ||
                          (isPremium && subscription?.plan.id === plan.id)
                        }
                      >
                        {plan.name} ({plan.price}/
                        {plan.billing_cycle === 'MONTHLY' ? 'mon' : 'yr'})
                      </Button>
                      <p className="text-xs text-gray-500">
                        {plan.description}
                      </p>
                    </div>
                  ))}

                  <Button
                    onClick={closeRenewModal}
                    className="block w-full mt-4"
                  >
                    Cancel
                  </Button>
                </div>
              </>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default SubscriptionStatus;
