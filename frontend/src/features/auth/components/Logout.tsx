import { Link, useNavigate } from 'react-router-dom';
import Button from '../../../components/common/Button';
import { useLogout } from '../hooks/useAuth';
import toast from 'react-hot-toast';

function Logout() {
  const { logout, isPending } = useLogout();
  const navigate = useNavigate();

  function handleSuccess() {
    navigate('/login');
  }

  function handleError(error: any) {
    toast.error(error.message || 'Something went wrong. Please try again.');
  }

  function handleLogout() {
    logout(undefined, {
      onSuccess: handleSuccess,
      onError: handleError,
    });
  }
  return (
    <>
      <Button variant="outline" disabled={isPending} onSubmit={handleLogout}>
        <Link to="/logout" aria-label="Logout of your account">
          Logout
        </Link>
      </Button>
    </>
  );
}

export default Logout;
