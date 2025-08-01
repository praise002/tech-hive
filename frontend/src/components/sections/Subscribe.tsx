import toast from 'react-hot-toast';
import Form from '../common/Form';
import Text from '../common/Text';

function Subscribe() {
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

  interface ResetFunction {
    (): void;
  }

  const handleFormSubmit = (data: FormData, reset: ResetFunction): void => {
    console.log('Form Data:', data);
    toast.success("You're all set! Thanks for subscribing to our newsletter.");
    reset();
  };

  return (
    <section className="px-0 sm:px-6 lg:px-8" id="subscribe">
      <div className="px-6 flex sm:flex-row flex-col sm:rounded-lg bg-light m-6 items-center justify-center py-8 gap-4 max-w-7xl mx-auto">
        <div className="flex-1 order-2 sm:order-none">
          <Text variant="h2" size="2xl" className="mb-4">
            Subscribe to Our <br />
            Newsletter
          </Text>
          <Form inputs={inputs} onSubmit={handleFormSubmit} className="w-full">
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
