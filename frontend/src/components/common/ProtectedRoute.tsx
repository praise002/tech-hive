import { useNavigate } from 'react-router-dom';

import { useEffect } from 'react';

import Spinner from './Spinner';

import { ProtectedRouteProps } from '../../types/types';
import { useCurrentUser } from '../../features/profile/hooks/useProfile';

// replace: true - Prevents the login page from being added to
// browser history, so users can't go back to protected routes after logout

// children: as prop (protected content)
function ProtectedRoute({ children }: ProtectedRouteProps) {
  const navigate = useNavigate();

  // 1. Load the authenticated user
  const { isPending, isAuthenticated } = useCurrentUser();

  // 2. If there is NO authenticated user, redirect to the /login
  useEffect(
    function () {
      if (!isAuthenticated && !isPending) navigate('/login', { replace: true });
    },
    [isAuthenticated, isPending, navigate]
  );

  // 3. While loading, show a spinner

  if (isPending)
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Spinner />
      </div>
    );

  // 4. If there IS a user, render the app
  if (isAuthenticated) return children;
}

export default ProtectedRoute;
