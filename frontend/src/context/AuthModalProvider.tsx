import { ReactNode, useState } from 'react';
import { AuthModalContext } from './AuthModalContext';

export function AuthModalProvider({ children }: { children: ReactNode }) {
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);
  const [redirectUrl, setRedirectUrl] = useState<string | null>(null);

  const openAuthModal = (url?: string) => {
    const urlToSave = url || window.location.pathname;
    setRedirectUrl(urlToSave);
    sessionStorage.setItem('authRedirectUrl', urlToSave);
    setIsAuthModalOpen(true);
  };

  const closeAuthModal = () => {
    setIsAuthModalOpen(false);
  };

  const clearRedirectUrl = () => {
    setRedirectUrl(null);
    sessionStorage.removeItem('authRedirectUrl');
  };

  return (
    <AuthModalContext.Provider
      value={{
        isAuthModalOpen,
        openAuthModal,
        closeAuthModal,
        redirectUrl,
        clearRedirectUrl,
      }}
    >
      {children}
    </AuthModalContext.Provider>
  );
}
