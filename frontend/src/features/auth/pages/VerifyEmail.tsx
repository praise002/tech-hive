import { RegisterOptions, UseFormSetError } from 'react-hook-form';
import Form from '../../../components/common/Form';
import Text from '../../../components/common/Text';
import { useRegisterOtp } from '../hooks/useAuth';
import toast from 'react-hot-toast';
import { useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { safeLocalStorage } from '../../../utils/utils';

interface FormData {
  email: string;
  otp: string;
}

function VerifyEmail() {
  const { verifyRegistrationOtp, isPending } = useRegisterOtp();
  const navigate = useNavigate();
  const [userEmail, setUserEmail] = useState('');
  const [showEmailInput, setShowEmailInput] = useState(false);

  useEffect(() => {
    // Get email from localStorage right when we need it
    const storage = safeLocalStorage();
    const savedEmail = storage.getItem('email');

    if (savedEmail) {
      setUserEmail(savedEmail);
      setShowEmailInput(false);
    } else {
      // No email found - show email input
      setShowEmailInput(true);
    }
  }, []);

  const inputs: Array<{
    name: keyof FormData;
    placeholder: string;
    type: string;
    rules: RegisterOptions<FormData>;
  }> = [
    // Show email input if we don't have it
    ...(showEmailInput
      ? [
          {
            name: 'email' as keyof FormData,
            placeholder: 'Enter your email address',
            type: 'email',
            rules: {
              required: 'Email is required',
              pattern: {
                value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                message: 'Invalid email address',
              },
            },
          },
        ]
      : []),
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

  const handleFormSubmit = (
    data: FormData,
    setError: UseFormSetError<FormData>
  ) => {
    console.log('Form Data:', data);

    // Use email from form if available, otherwise use saved email
    const emailToUse = showEmailInput ? data.email : userEmail;

    // Additional safety check
    if (!emailToUse) {
      toast.error('Email is required. Please refresh the page and try again.');
      return;
    }

    // Combine localStorage email with form OTP
    const verificationData: FormData = {
      email: emailToUse,
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
  };

  return (
    <div className="px-4 sm:px-6 lg:px-8 py-22 dark:text-white">
      <Text variant="h2" size="2xl" className="mb-1 dark:text-white">
        Verify Email
      </Text>
      <p className="text-secondary text-sm mb-4">
        {showEmailInput
          ? 'Enter your email address and the verification code sent to your email.'
          : `Check your email for a verification code and enter it below.`}
      </p>
      <Form
        inputs={inputs}
        onSubmit={handleFormSubmit}
        isLoading={isPending}
        className="w-full"
      >
        Verify OTP
      </Form>
      <p className="text-secondary text-sm mt-2">
        To receive a new otp <a href="#">Click Here!</a>
      </p>
    </div>
  );
}

export default VerifyEmail;
