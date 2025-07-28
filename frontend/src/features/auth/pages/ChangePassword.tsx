import Form from '../../../components/common/Form';
import Text from '../../../components/common/Text';

interface ChangePasswordFormData {
  currentPassword: string;
  newPassword: string;
  password: string;
}

function ChangePassword() {
  const inputs: Array<{
    name: keyof ChangePasswordFormData;
    placeholder: string;
    type: string;
    rules: any;
  }> = [
    {
      name: 'currentPassword',
      placeholder: 'Current Password',
      type: 'password',
      rules: {
        required: 'Password is required',
        // Backend will check if the password is correct
      },
    },
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
    }, // Backend will confirm if they are the same
  ];

  const handleFormSubmit = (
    data: ChangePasswordFormData,
    reset: () => void
  ) => {
    console.log('Form Data:', data);
    alert('Password Changed successfully!');
    reset();
  };

  return (
    <div className="px-4 sm:px-6 lg:px-8 py-20">
      <Text variant="h2" size="2xl" className="mb-4 dark:text-custom-white">
        Change Password
      </Text>
      <Form inputs={inputs} onSubmit={handleFormSubmit} className="w-full">
        Update Password
      </Form>
    </div>
  );
}

export default ChangePassword;
