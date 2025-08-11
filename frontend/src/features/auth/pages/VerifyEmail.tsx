import Form from "../../../components/common/Form";
import Text from "../../../components/common/Text";

interface FormData {
  otp: string;
}

function VerifyEmail() {
  const Input: Array<{
    name: keyof FormData;
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

  const handleFormSubmit = (
    data: FormData,
    reset: () => void
  ) => {
    console.log('Form Data:', data);
    alert('Form Submitted successfully!');
    reset();
  };

  return (
      <div className="px-4 sm:px-6 lg:px-8 my-20">
        <Text variant="h2" size="2xl" className="mb-1">
          Verify Email
        </Text>
        <p className="text-secondary text-sm mb-4">
          Check your email for a verification code and enter it below.
        </p>
        <Form
          inputs={Input}
          onSubmit={handleFormSubmit}
          className="w-full"
        >
          Verify OTP
        </Form>
        <p className="text-secondary text-sm mt-2">
          To receive a new otp <a href="#">Click Here!</a>
        </p>
      </div>
    );
}

export default VerifyEmail;

