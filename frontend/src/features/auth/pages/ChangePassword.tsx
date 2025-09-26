import { UseFormSetError } from 'react-hook-form';
import Form from '../../../components/common/Form';
import Text from '../../../components/common/Text';
import { useChangePassword } from '../hooks/useAuth';
import toast from 'react-hot-toast';

interface ChangePasswordFormData {
  currentPassword: string;
  newPassword: string;
  password: string;
}

interface ChangePasswordApiData {
  old_password: string;
  new_password: string;
  confirm_password: string;
}

function ChangePassword() {
  const { changePassword, isPending } = useChangePassword();

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
    },
  ];

  const handleFormSubmit = (
    data: ChangePasswordFormData,
    setError: UseFormSetError<ChangePasswordFormData>
  ) => {
    console.log('Form Data:', data);
    alert('Password Changed successfully!');

    const changePasswordData: ChangePasswordApiData = {
      old_password: data.currentPassword,
      new_password: data.newPassword,
      confirm_password: data.password,
    };

    changePassword(changePasswordData, {
      onSuccess: (response) => {
        toast.success(response?.message);
      },
      onError: (error: any) => {
        // Handle field-specific errors from the server
        if (error.data) {
          const fieldMapping: Record<string, keyof ChangePasswordFormData> = {
            old_password: 'currentPassword',
            new_password: 'newPassword',
            confirm_password: 'password',
          };

          Object.entries(error.data).forEach(([field, message]) => {
            const formField =
              fieldMapping[field] || (field as keyof ChangePasswordFormData);
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
    <div className="px-4 sm:px-6 lg:px-8 py-20">
      <Text variant="h2" size="2xl" className="mb-4 dark:text-custom-white">
        Change Password
      </Text>
      <Form inputs={inputs} onSubmit={handleFormSubmit} isLoading={isPending} className="w-full">
        Update Password
      </Form>
    </div>
  );
}

export default ChangePassword;
