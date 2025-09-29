import { RegisterOptions, UseFormSetError } from 'react-hook-form';
import Form from '../../../components/common/Form';
import Text from '../../../components/common/Text';
import {
  useEmail,
  useRegisterOtp,
  useRegisterResendOtp,
} from '../hooks/useAuth';
import toast from 'react-hot-toast';
import { useLocation, useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';

interface FormData {
  email: string;
  otp: string;
}

interface LocationState {
  email?: string;
}

function VerifyEmail() {
  const [resendCooldown, setResendCooldown] = useState(0);
  const { verifyRegistrationOtp, isPending } = useRegisterOtp();
  const { resendRegistrationOtp, isPending: isResending } =
    useRegisterResendOtp();
  const { getEmail } = useEmail();
  const navigate = useNavigate();
  const location = useLocation();

  const state = location.state as LocationState;
  const email = (getEmail() as string) || state?.email;

  useEffect(() => {
    if (resendCooldown > 0) {
      const timer = setTimeout(() => {
        setResendCooldown(resendCooldown - 1);
      }, 1000);
      return () => clearTimeout(timer);
    }
  }, [resendCooldown]);

  const inputs: Array<{
    name: keyof FormData;
    placeholder: string;
    type: string;
    rules: RegisterOptions<FormData>;
  }> = [
    // Show email input if we don't have it

    {
      name: 'otp',
      placeholder: 'Enter OTP',
      type: 'text',
      rules: {
        required: 'OTP is required',
        minLength: {
          value: 6,
          message: 'OTP must be 6 digits',
        },
        maxLength: {
          value: 6,
          message: 'OTP must be 6 digits',
        },
        pattern: {
          value: /^[0-9]+$/,
          message: 'OTP must contain only numbers',
        },
      },
    },
  ];

  function handleFormSubmit(
    data: FormData,
    setError: UseFormSetError<FormData>
  ) {
    console.log('Form Data:', data);

    // Additional safety check
    if (!email) {
      toast.error('Email not found. Please try registering again.');
      return;
    }

    // Combine cache email with form OTP
    const verificationData: FormData = {
      email: email,
      otp: data.otp,
    };

    verifyRegistrationOtp(verificationData, {
      onSuccess: (response) => {
        toast.success(response?.message);
        // Navigate to page to login
        navigate('/login'); // Only if still on this page
      },
      onError: (error: any) => {
        // Handle field-specific errors from the server
        if (error.data) {
          const fieldMapping: Record<string, keyof FormData> = {
            email: 'email',
            otp: 'otp',
          };

          Object.entries(error.data).forEach(([field, message]) => {
            const formField = fieldMapping[field] || (field as keyof FormData);
            setError(formField, {
              type: 'server',
              message: Array.isArray(message) ? message[0] : String(message),
            });
          });
        } else {
          // Handle general errors (no specific field)
          toast.error(
            error.message || 'Something went wrong. Please try again.'
          );
        }
      },
    });
  }

  function handleResendOtp() {
    if (!email) {
      toast.error('Email not found. Please try registering again.');
      return;
    }
    resendRegistrationOtp(email, {
      onSuccess: (response) => {
        toast.success(response?.message);
        setResendCooldown(60);
      },
      onError: (error: any) => {
        toast.error(error.message);
      },
    });
  }

  return (
    <div className="px-4 sm:px-6 lg:px-8 py-22 dark:text-white">
      <Text variant="h2" size="2xl" className="mb-1 dark:text-white">
        Verify Email
      </Text>
      <p className="text-secondary text-sm mb-4">
        Check your email for a verification code and enter it below.
      </p>
      <Form
        inputs={inputs}
        onSubmit={handleFormSubmit}
        isLoading={isPending}
        className="w-full"
      >
        Verify OTP
      </Form>
      <div className="text-secondary text-sm mt-2">
        {resendCooldown > 0 ? (
          <span>Resend OTP in {resendCooldown} seconds</span>
        ) : (
          <span>
            Didn't receive OTP?{' '}
            <button
              type="button"
              onClick={handleResendOtp}
              disabled={isResending || resendCooldown > 0}
              className={`underline ${
                isResending ? 'cursor-not-allowed' : 'cursor-pointer'
              }`}
            >
              {isResending ? 'Sending...' : 'Click Here to Resend'}
            </button>
          </span>
        )}
      </div>
    </div>
  );
}

export default VerifyEmail;
