import { useForm } from 'react-hook-form';
import Text from './Text';
import Button from './Button';
import toast from 'react-hot-toast';
import { useSendContactMessage } from '../../hooks/useGeneral';
import Spinner from './Spinner';
import { handleMutationError } from '../../utils/errorHandler';

interface ContactFormData {
  firstName: string;
  lastName: string;
  email: string;
  message: string;
}

function ContactForm() {
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    setError,
  } = useForm<ContactFormData>();

  const { sendContactMessage, isPending } = useSendContactMessage();

  const onSubmit = (data: ContactFormData) => {
    const contactData = {
      name: `${data.firstName} ${data.lastName}`.trim(),
      email: data.email,
      content: data.message,
    };

    sendContactMessage(contactData, {
      onSuccess: (response: any) => {
        toast.success(response?.message || 'Message sent successfully!');
        reset();
      },
      onError: (error: any) => {
        const fieldMapping: Record<string, keyof ContactFormData> = {
          name: 'firstName',
          email: 'email',
          content: 'message',
        };

        const errorMessage = handleMutationError(error, setError, fieldMapping);
        if (!error.data) {
          toast.error(errorMessage);
        }
      },
    });
  };

  return (
    <div className="px-4 sm:px-6 lg:px-8 py-20">
      <form
        className="space-y-4 dark:text-custom-white"
        onSubmit={handleSubmit(onSubmit)}
      >
        <Text variant="h2" size="2xl" className="sm:xl dark:text-custom-white">
          Contact Form
        </Text>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <div>
            <input
              type="text"
              id="firstName"
              placeholder="First Name"
              aria-label="First Name"
              {...register('firstName', { required: 'First name is required' })}
              className="appearance-none block w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-800 dark:bg-dark-bg"
              disabled={isPending}
            />
            {errors.firstName && (
              <p className="text-red-500 text-sm mt-1" role="alert">
                {errors.firstName?.message as string}
              </p>
            )}
          </div>
          <div>
            <input
              id="lastName"
              placeholder="Last Name"
              aria-label="Last Name"
              {...register('lastName', { required: 'Last name is required' })}
              className="appearance-none block w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-800 dark:bg-dark-bg"
              disabled={isPending}
            />
            {errors.lastName && (
              <p className="text-red-500 text-sm mt-1" role="alert">
                {errors.lastName?.message as string}
              </p>
            )}
          </div>
        </div>

        <div>
          <input
            id="email"
            type="email"
            placeholder="Email"
            aria-label="Email address"
            {...register('email', {
              required: 'Email is required',
              pattern: {
                value: /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/,
                message: 'Invalid email address',
              },
            })}
            className="appearance-none block w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-800 dark:bg-dark-bg"
            disabled={isPending}
          />
          {errors.email && (
            <p className="text-red-500 text-sm mt-1" role="alert">
              {errors.email.message as string}
            </p>
          )}
        </div>

        <div>
          <textarea
            id="message"
            placeholder="What can we help you with?"
            aria-label="Message"
            {...register('message', { required: 'Message is required' })}
            className="block w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-800 dark:bg-dark-bg"
            rows={4}
            disabled={isPending}
          />
          {errors.message && (
            <p className="text-red-500 text-sm mt-1" role="alert">
              {errors.message.message as string}
            </p>
          )}
        </div>

        <Button type="submit" variant="primary" disabled={isPending}>
          {isPending ? (
            <div className="flex items-center justify-center gap-2">
              <Spinner />
              <span>Sending...</span>
            </div>
          ) : (
            'Send Message'
          )}
        </Button>
      </form>
    </div>
  );
}

export default ContactForm;
