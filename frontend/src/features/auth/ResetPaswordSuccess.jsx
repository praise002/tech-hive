import Button from '../../components/common/Button';

function ResetPasswordSuccess() {
  return (
    <div className="dark:text-custom-white text-center min-h-[calc(100vh-400px)] px-4 sm:px-6 lg:px-8 py-20">
      <p className="font-bold text-lg">Password Reset Successful!</p>
      <p className='my-1'>You can now log in with your new credentials.</p>
      <Button
        type="submit"
        variant="outline"
        onClick={() => alert('Redirecting to Login')}
      >
        Login
      </Button>
    </div>
  );
}

export default ResetPasswordSuccess;
