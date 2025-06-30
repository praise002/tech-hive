import { IoEye, IoEyeOff } from 'react-icons/io5';
import { FcGoogle } from 'react-icons/fc';
import { FaApple } from 'react-icons/fa';
import { Link } from 'react-router-dom';
import Button from '../../components/common/Button';
import Form from '../../components/common/Form';
import { useState } from 'react';

interface LoginFormData {
  email: string;
  password: string;
}

function LoginForm() {
  const [showPassword, setShowPassword] = useState(false);

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
  const handleFormSubmit = (data: LoginFormData, reset: () => void) => {
    console.log('Form Data:', data);
    alert('Form Submitted successfully!');
    reset();
  };
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

        <Form inputs={inputs} onSubmit={handleFormSubmit} className="w-full">
          Register
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
          >
            <FcGoogle className="text-xl" />
            <span>Register with Google</span>
          </Button>
        </div>

        <div className="my-4">
          <Button
            className="w-full flex items-center justify-center gap-2"
            variant="outline"
          >
            <FaApple className="text-xl text-black" />
            <span>Register with Apple</span>
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
