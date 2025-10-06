import { IoEye, IoEyeOff } from 'react-icons/io5';
import { FcGoogle } from 'react-icons/fc';
import { FaApple } from 'react-icons/fa';
import { Link, useNavigate } from 'react-router-dom';

import { useState } from 'react';
import Form from '../../../components/common/Form';
import Button from '../../../components/common/Button';
import { useGoogleLogin, useLogin } from '../hooks/useAuth';
import { UseFormSetError } from 'react-hook-form';
import toast from 'react-hot-toast';

interface LoginFormData {
  email: string;
  password: string;
}

function LoginForm() {
  const [showPassword, setShowPassword] = useState(false);
  const { login, isPending } = useLogin();
  const { fetchAuthLoginUrl, isPending: isGooglePending } = useGoogleLogin();
  const navigate = useNavigate();

  function handleGoogleLogin() {
    fetchAuthLoginUrl(undefined, {
      onSuccess: (authorizationUrl) => {
        window.location.href = authorizationUrl;
      },
      onError: () => {
        toast.error('Failed to start Google login. Please try again.');
      },
    });
  }

  function togglePasswordVisibility() {
    setShowPassword(!showPassword);
  }

  const inputs: Array<{
    name: keyof LoginFormData;
    placeholder: string;
    type: string;
    rules: any;
    icon?: React.ReactNode;
    onIconClick?: () => void;
    iconAriaLabel?: string;
  }> = [
    {
      name: 'email',
      placeholder: 'Email',
      type: 'email',
      rules: {
        required: 'Email is required',
        pattern: {
          value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
          message: 'Invalid email address',
        },
      },
    },
    {
      name: 'password',
      type: showPassword ? 'text' : 'password',
      placeholder: 'Password',
      icon: showPassword ? (
        <IoEyeOff className="text-primary cursor-pointer" />
      ) : (
        <IoEye className="text-primary cursor-pointer" />
      ),
      onIconClick: togglePasswordVisibility,
      iconAriaLabel: showPassword ? 'Hide password' : 'Show password',
      rules: {
        required: 'Password is required',
        minLength: {
          value: 6,
          message: 'Password must be at least 6 characters',
        },
      },
    },
  ];

  function handleFormSubmit(
    data: LoginFormData,
    setError: UseFormSetError<LoginFormData>
  ) {
    console.log('Form Data:', data);

    const loginData: LoginFormData = {
      email: data.email,
      password: data.password,
    };

    login(loginData, {
      onSuccess: (response) => {
        toast.success(response?.message);
        navigate('/'); // Only if still on this page
      },
      onError: (error: any) => {
        // Handle field-specific errors from the server
        if (error.data) {
          const fieldMapping: Record<string, keyof LoginFormData> = {
            email: 'email',
            password: 'password',
          };

          Object.entries(error.data).forEach(([field, message]) => {
            const formField =
              fieldMapping[field] || (field as keyof LoginFormData);
            setError(formField, {
              type: 'server',
              message: Array.isArray(message) ? message[0] : String(message),
            });
          });
        } else {
          if (
            error.message &&
            error.message.toLowerCase().includes('disabled') &&
            error.status === 403
          ) {
            navigate('/account-disabled');
            return;
          } else if (
            error.message &&
            error.message.toLowerCase().includes('not verified') &&
            error.status === 403
          ) {
            toast.error('Account not verified.');
            navigate('/verify-email', {
              state: { email: data.email },
            });
            return;
          }

          toast.error(
            error.message || 'Something went wrong. Please try again.'
          );
        }
      },
    });
  }

  return (
    <div className="px-4 sm:px-6 lg:px-8 py-20 flex flex-col md:flex-row">
      <div className="md:flex-1">
        <img
          src="/assets/abstract-network-com-bg.jpg"
          className="w-full h-full object-cover"
          alt="Abstract Network Background"
        />
      </div>

      <div className="bg-light md:flex-1 p-6">
        <div className="uppercase text-gray-900 text-xl font-bold">
          Tec<span className="text-red-700">Hive.</span>
        </div>
        <div className="flex items-center gap-2 my-4">
          <div className="text-secondary">
            <Link to="/register">Register</Link>
          </div>
          <div className="h-4 w-[1px] bg-red"></div>
          <div className="text-primary">
            <Link to="/login">Login</Link>
          </div>
        </div>

        <Form
          inputs={inputs}
          onSubmit={handleFormSubmit}
          isLoading={isPending}
          className="w-full"
        >
          Login
        </Form>

        <div className="my-4 flex items-center gap-2">
          <div className="flex-1">
            <hr className="border-b-1 border-color-text-primary" />
          </div>
          <div className="uppercase text-primary">or</div>
          <div className="flex-1">
            <hr className="border-b-1 border-color-text-primary" />
          </div>
        </div>

        <div>
          <Button
            className="w-full flex items-center justify-center gap-2"
            variant="outline"
            onClick={handleGoogleLogin}
            disabled={isGooglePending}
          >
            <FcGoogle className="text-xl" />
            <span>Login with Google</span>
          </Button>
        </div>

        <div className="my-4">
          <Button
            className="w-full flex items-center justify-center gap-2"
            variant="outline"
            onClick={handleGoogleLogin}
            disabled={isGooglePending}
          >
            <FaApple className="text-xl text-black" />
            <span>Login with Apple</span>
          </Button>
        </div>

        <p className="text-primary text-xs">
          By signing up, you are agreeing to our{' '}
          <span className="text-red">privacy policy</span> and{' '}
          <span className="text-red">terms of use.</span>
        </p>
      </div>
    </div>
  );
}

export default LoginForm;

// IF EMAIL NOT VERIFIED, SINCE THIS IS A MULTI-STEP PROCESS, AND THE POSSIBILITY IS LOW
// 1. Redirect to verify-email page if email not verified
// 2. API should return the email if email not verified which can be used to send verification
