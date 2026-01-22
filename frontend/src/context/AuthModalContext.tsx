import { createContext, useContext } from 'react';

interface AuthModalContextType {
  isAuthModalOpen: boolean;
  openAuthModal: (redirectUrl?: string) => void;
  closeAuthModal: () => void;
  redirectUrl: string | null;
  clearRedirectUrl: () => void;
}

export const AuthModalContext = createContext<AuthModalContextType | undefined>(
  undefined
);

export function useAuthModal() {
  const context = useContext(AuthModalContext);
  if (context === undefined) {
    throw new Error('useAuthModal must be used within an AuthModalProvider');
  }
  return context;
}
