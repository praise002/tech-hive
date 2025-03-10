import Form from '../common/Form';
import Text from '../common/Text';

function Subscribe() {
  const inputs = [
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

  const handleFormSubmit = (data) => {
    console.log('Form Data:', data);
    alert('Form submitted successfully!');
  };

  return (
    <div className="px-0 sm:px-6 lg:px-8" id="subscribe">
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
            src="/src/assets/realistic-post-mailbox-letter-hand-composition-with-human-hand-envelopes-classic-mail-box_1284-26890-removebg-preview 1.png"
            alt="mailbox"
            className="max-w-full h-auto"
          />
        </div>
      </div>
    </div>
  );
}

// TODO: BUTTON CHANGES TO SUBSCRIBED

export default Subscribe;
