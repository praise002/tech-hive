import toast from 'react-hot-toast';
import { useNavigate } from 'react-router-dom';
import { useLogoutAll } from '../hooks/useAuth';
import Button from '../../../components/common/Button';

function LogoutAll() {
  const { logoutAll, isPending } = useLogoutAll();
  const navigate = useNavigate();

  function handleSuccess() {
    navigate('/login');
  }

  function handleError(error: any) {
    toast.error(error.message || 'Something went wrong. Please try again.');
  }

  function handleLogoutAll() {
    const confirmed = confirm(
      "This will log you out of all devices and browsers. You'll need to log in again everywhere. Continue?"
    );

    if (confirmed) {
      logoutAll(undefined, {
        onSuccess: handleSuccess,
        onError: handleError,
      });
    }
  }

  return (
    <>
      <Button variant="outline" onClick={handleLogoutAll} disabled={isPending}>
        Log out all devices
      </Button>
    </>
  );
}

export default LogoutAll;
