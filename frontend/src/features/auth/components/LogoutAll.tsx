import toast from 'react-hot-toast';
import { useNavigate } from 'react-router-dom';
import { useLogoutAll } from '../hooks/useAuth';
import Button from '../../../components/common/Button';

function LogoutAll() {
  const navigate = useNavigate();

  function handleUnauthenticated() {
    navigate('/login');
  }

  const { logoutAll, isPending } = useLogoutAll(handleUnauthenticated);

  function handleSuccess() {
    navigate('/login');
  }

  function handleError(error: any) {
    toast.error(error.message || 'Something went wrong. Please try again.');
  }

  function handleLogoutAll() {
    toast(
      (t) => (
        <div className="flex flex-col gap-2">
          <p className="text-sm font-medium text-gray-900">
            Log out from all devices?
          </p>
          <p className="text-xs text-gray-500 mb-2">
            You'll need to log in again everywhere.
          </p>
          <div className="flex gap-2 justify-end">
            <button
              onClick={() => toast.dismiss(t.id)}
              className="px-3 py-1 text-xs font-medium text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded transition-colors"
            >
              Cancel
            </button>
            <button
              onClick={() => {
                toast.dismiss(t.id);
                logoutAll(undefined, {
                  onSuccess: handleSuccess,
                  onError: handleError,
                });
              }}
              className="px-3 py-1 text-xs font-medium bg-red-600 text-white hover:bg-red-700 rounded shadow-sm transition-colors"
            >
              Log out
            </button>
          </div>
        </div>
      ),
      {
        duration: 10000,
        position: 'top-center',
      }
    );
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
