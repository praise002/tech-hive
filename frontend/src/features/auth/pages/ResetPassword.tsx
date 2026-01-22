import { useState, useEffect } from 'react';
import Form from '../../../components/common/Form';
import Text from '../../../components/common/Text';
import { UseFormSetError } from 'react-hook-form';
import {
  useCompletePasswordReset,
  useRequestPasswordReset,
  useVerifyPasswordResetOtp,
} from '../hooks/useAuth';
import toast from 'react-hot-toast';

import { safeLocalStorage } from '../../../utils/utils';
import { useNavigate } from 'react-router-dom';

interface EmailFormData {
  email: string;
}

interface OtpFormData {
  otp: string;
}

interface SetNewPasswordFormData {
  newPassword: string;
  confirmPassword: string;
}

function ResetPassword() {
  const { requestPasswordReset, isPending: isRequestPending } =
    useRequestPasswordReset();
  const { verifyPasswordResetOtp, isPending: isVerifyPending } =
    useVerifyPasswordResetOtp();
  const { completePasswordReset, isPending: isCompletePending } =
    useCompletePasswordReset();

  const [step, setStep] = useState(1); // Step 1: Email input, Step 2: OTP, Step 3: Set new password 4: Password reset complete
  const [ticker, setTicker] = useState(60);
  const [canResend, setCanResend] = useState(false);

  const navigate = useNavigate();
  const storage = safeLocalStorage();

  useEffect(() => {
    let interval: ReturnType<typeof setInterval>;
    if (step === 2 && ticker > 0) {
      interval = setInterval(() => {
        setTicker((prev) => prev - 1);
      }, 1000);
    } else if (ticker === 0) {
      setCanResend(true);
    }

    return () => clearInterval(interval);
  }, [step, ticker]);

  function handleNextStep() {
    if (step < 4) setStep((s) => s + 1);
  }

  function handleResendOtp() {
    const email = storage.getItem('email');
    if (!email) {
      toast.error('Email not found. Please start over.');
      setStep(1);
      return;
    }

    requestPasswordReset(email, {
      onSuccess: (response) => {
        toast.success(response?.message || 'OTP resent successfully');
        setTicker(60);
        setCanResend(false);
      },
      onError: (error: any) => {
        toast.error(error?.message || 'Failed to resend OTP');
      },
    });
  }

  const emailInput: Array<{
    name: keyof EmailFormData;
    placeholder: string;
    type: string;
    rules: any;
  }> = [
    {
      name: 'email',
      placeholder: 'jack@example.com',
      type: 'email',
      rules: {
        required: 'Email is required',
        pattern: {
          value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
          message: 'Invalid email address',
        },
      },
    },
  ];

  const otpInput: Array<{
    name: keyof OtpFormData;
    placeholder: string;
    type: string;
    rules: any;
  }> = [
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

  const setNewPasswordInput: Array<{
    name: keyof SetNewPasswordFormData;
    placeholder: string;
    type: string;
    rules: any;
  }> = [
    {
      name: 'newPassword',
      placeholder: 'New Password',
      type: 'password',
      rules: {
        required: 'Password is required',
        minLength: {
          value: 6,
          message: 'Password must be at least 6 characters',
        },
      },
    },
    {
      name: 'confirmPassword',
      placeholder: 'Confirm New Password',
      type: 'password',
      rules: {
        required: 'Password is required',
        minLength: {
          value: 6,
          message: 'Password must be at least 6 characters',
        },
      },
    },
  ];

  const handleFormSubmit = (
    data: EmailFormData | OtpFormData | SetNewPasswordFormData,
    setError: UseFormSetError<
      EmailFormData | OtpFormData | SetNewPasswordFormData
    >
  ) => {
    if (step === 1 && 'email' in data) {
      requestPasswordReset(data.email, {
        onSuccess: (response) => {
          toast.success(response?.message || 'OTP sent to your email');
          handleNextStep();
          setTicker(60); // Start timer when moving to step 2
          setCanResend(false);
        },
        onError: (error: any) => {
          const fieldMapping: Record<string, keyof EmailFormData> = {
            email: 'email',
          };

          Object.entries(error.data).forEach(([field, message]) => {
            const formField =
              fieldMapping[field] || (field as keyof EmailFormData);
            setError(formField, {
              type: 'server',
              message: Array.isArray(message) ? message[0] : String(message),
            });
          });
        },
      });
    } else if (step === 2 && 'otp' in data) {
      const email = storage.getItem('email');
      if (!email) {
        toast.error('Email not found. Please start over.');
        setStep(1);
        return;
      }

      const otpData = {
        email,
        otp: data.otp,
      };
      verifyPasswordResetOtp(otpData, {
        onSuccess: (response) => {
          toast.success(response?.message || 'OTP verified successfully');
          handleNextStep();
        },
        onError: (error: any) => {
          toast.error(error?.message);
        },
      });
    } else if (
      step === 3 &&
      'newPassword' in data &&
      'confirmPassword' in data
    ) {
      const email = storage.getItem('email');
      if (!email) {
        toast.error('Email not found. Please start over.');
        setStep(1);
        return;
      }
      const resetData = {
        email,
        new_password: data.newPassword,
        confirm_password: data.confirmPassword,
      };
      completePasswordReset(resetData, {
        onSuccess: (response) => {
          toast.success(response?.message || 'Password reset successfully');
          navigate('/login');
        },
        onError: (error: any) => {
          toast.error(error?.message);
        },
      });
    }
  };

  if (step === 1) {
    return (
      <div className="px-4 sm:px-6 lg:px-8 my-20">
        <Text variant="h2" size="2xl" className="mb-4 dark:text-custom-white">
          Reset Password
        </Text>
        <Form
          inputs={emailInput}
          onSubmit={handleFormSubmit}
          isLoading={isRequestPending}
          className="w-full"
        >
          Send OTP
        </Form>
      </div>
    );
  }

  if (step === 2) {
    return (
      <div className="px-4 sm:px-6 lg:px-8 my-20">
        <Text variant="h2" size="2xl" className="mb-1 dark:text-custom-white">
          Reset your Password
        </Text>
        <p className="text-secondary text-sm mb-4 dark:text-custom-gray-300">
          Check your email for a verification code and enter it below.
        </p>
        <Form
          inputs={otpInput}
          onSubmit={handleFormSubmit}
          isLoading={isVerifyPending}
          className="w-full"
        >
          Verify OTP
        </Form>
        <p className="text-secondary text-sm mt-2">
          To receive a new otp{' '}
          {canResend ? (
            <button
              type="button"
              className="text-primary dark:text-custom-white hover:underline cursor-pointer bg-transparent border-none p-0 inline font-medium"
              onClick={handleResendOtp}
              disabled={isRequestPending}
            >
              Click Here!
            </button>
          ) : (
            <span className="text-gray-400">in {ticker}s</span>
          )}
        </p>
      </div>
    );
  }

  if (step === 3) {
    return (
      <div className="px-4 sm:px-6 lg:px-8 py-20">
        <Text variant="h2" size="2xl" className="mb-1 dark:text-custom-white">
          Reset your Password
        </Text>
        <p className="text-secondary text-sm mb-4 dark:text-custom-gray-300">
          Please enter your new password twice:
        </p>
        <Form
          inputs={setNewPasswordInput}
          onSubmit={handleFormSubmit}
          isLoading={isCompletePending}
          className="w-full"
        >
          Set New Password
        </Form>
      </div>
    );
  }

  return;
}

export default ResetPassword;
