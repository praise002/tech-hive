import toast from 'react-hot-toast';
import Form from '../common/Form';
import Text from '../common/Text';
import { UseFormSetError } from 'react-hook-form';
import { useSubscribeNewsletter } from '../../hooks/useGeneral';

function Subscribe() {
  const { subscribeNewsletter, isPending } = useSubscribeNewsletter();

  const inputs: Array<{
    name: keyof FormData;
    placeholder: string;
    type: string;
    ariaLabel: string;
    rules: any;
  }> = [
    {
      name: 'email',
      placeholder: 'jack@example.com',
      type: 'email',
      ariaLabel: 'Email address',
      rules: {
        required: 'Email is required',
        pattern: {
          value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
          message: 'Invalid email address',
        },
      },
    },
  ];

  interface FormData {
    email: string;
  }

  const handleFormSubmit = (
    data: FormData,
    setError: UseFormSetError<FormData>,
    reset?: () => void
  ): void => {
    reset?.();

    subscribeNewsletter(data.email, {
      onSuccess: (response) => {
        toast.success(response?.message);
      },
      onError: (error: any) => {
        // Handle field-specific errors from the server
        if (error.data) {
          const fieldMapping: Record<string, keyof FormData> = {
            email: 'email',
          };

          Object.entries(error.data).forEach(([field, message]) => {
            const formField = fieldMapping[field] || (field as keyof FormData);
            setError(formField, {
              type: 'server',
              message: Array.isArray(message) ? message[0] : String(message),
            });
          });
        }
      },
    });
  };

  return (
    <section className="px-0 sm:px-6 lg:px-8" id="subscribe">
      <div className="px-6 flex sm:flex-row flex-col sm:rounded-lg bg-light m-6 items-center justify-center py-8 gap-4 max-w-7xl mx-auto">
        <div className="flex-1 order-2 sm:order-none">
          <Text variant="h2" size="2xl" className="mb-4">
            Subscribe to Our <br />
            Newsletter
          </Text>
          <Form
            inputs={inputs}
            onSubmit={handleFormSubmit}
            isLoading={isPending}
            className="w-full"
          >
            Subscribe
          </Form>
        </div>
        <div className="flex-1 order-1 sm:order-none">
          <img
            src="/assets/realistic-post-mailbox-letter-hand-composition-with-human-hand-envelopes-classic-mail-box_1284-26890-removebg-preview 1.png"
            alt="mailbox"
            className="max-w-full h-auto"
          />
        </div>
      </div>
    </section>
  );
}

export default Subscribe;
