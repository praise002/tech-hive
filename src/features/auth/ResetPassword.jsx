import { useState } from 'react';
import Form from '../../components/common/Form';
import Text from '../../components/common/Text';

function ResetPassword() {
  const [step, setStep] = useState(3); // Step 1: Email input, Step 2: OTP, Step 3: Set new password 4: Password reset complete

  function handleNextStep() {
    if (step < 4) setStep((s) => s + 1);
  }

  const emailInput = [
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

  const otpInput = [
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
  const setNewPasswordInput = [
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
      name: 'password',
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

  const handleFormSubmit = (data) => {
    console.log('Form Data:', data);
    alert('Form Submitted successfully!');
  };

  if (step === 1) {
    return (
      <div className="px-4 sm:px-6 lg:px-8 my-20">
        <Text variant="h2" size="2xl" className="mb-4">
          Reset Password
        </Text>
        <Form
          inputs={emailInput}
          onClick={handleNextStep}
          onSubmit={handleFormSubmit}
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
        <Text variant="h2" size="2xl" className="mb-1">
          Reset your Password
        </Text>
        <p className="text-color-text-secondary text-sm mb-4">
          Check your email for a verification code and enter it below.
        </p>
        <Form
          inputs={otpInput}
          onClick={handleNextStep}
          onSubmit={handleFormSubmit}
          className="w-full"
        >
          Verify OTP
        </Form>
        <p className="text-color-text-secondary text-sm mt-2">
          To receive a new otp <a href="#">Click Here!</a>
        </p>
      </div>
    );
  }

  if (step === 3) {
    return (
      <div className="px-4 sm:px-6 lg:px-8 my-20">
        <Text variant="h2" size="2xl" className="mb-1">
          Reset your Password
        </Text>
        <p className="text-color-text-secondary text-sm mb-4">
          Please enter your new password twice:
        </p>
        <Form
          inputs={setNewPasswordInput}
          onClick={handleNextStep}
          onSubmit={handleFormSubmit}
          className="w-full"
        >
          Set New Password
        </Form>
      </div>
    );
  }
}

export default ResetPassword;
