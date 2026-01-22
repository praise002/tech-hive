import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';

import About from './pages/About';
import AccountDetail from './features/profile/pages/AccountDetail';
import AppLayout from './components/Layouts/AppLayout';

import CategoryDetail from './features/category/CategoryDetail';
import CategoryList from './features/category/CategoryList';
import Contact from './pages/Contact';

import Home from './pages/Home';
import Login from './features/auth/pages/Login';
import PageNotFound from './pages/PageNotFound';
import Unsubscribe from './pages/Unsubscribe';

import Register from './features/auth/pages/Register';
import TechEventList from './features/events/TechEventList';
import TechEventDetail from './features/events/TechEventDetail';

import TechJobDetail from './features/jobs/TechJobDetail';
import TechJobsList from './features/jobs/TechJobsList';
import TechToolDetail from './features/tools/TechToolDetail';
import TechToolList from './features/tools/TechToolList';

import ResourceList from './features/resource/ResourceList';
import ResourceDetail from './features/resource/ResourceDetail';
import ChangePassword from './features/auth/pages/ChangePassword';
import ResetPassword from './features/auth/pages/ResetPassword';
import ResetPasswordSuccess from './features/auth/pages/ResetPaswordSuccess';
import { Toaster } from 'react-hot-toast';

import AdminDashboard from './features/admin/pages/AdminDashboard';

import Liveblock from './features/articles/pages/Liveblock';
import Docs from './features/articles/pages/Docs';
import ComingSoon from './pages/coming-soon';
import CampusKart from './pages/CampusKart';
import ArticleList from './features/articles/pages/ArticleList';

import VerifyEmail from './features/auth/pages/VerifyEmail';
import ProtectedRoute from './components/common/ProtectedRoute';
import ProfileDetail from './features/profile/pages/ProfileDetail';
import AccountDisabled from './features/auth/pages/AccountDisabled';
import Logout from './features/auth/components/Logout';
import NotificationList from './features/notifications/pages/NotificationList';
import { AuthModalProvider } from './context/AuthModalProvider';
import AuthModal from './features/auth/components/AuthModal';
import {
  GoogleLoginCallback,
  GoogleRegisterCallback,
} from './features/auth/pages/GoogleCallback';
import PaymentStatus from './features/subscription/pages/PaymentStatus';
import ArticleDetail from './features/articles/pages/ArticleDetail';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ReactQueryDevtools initialIsOpen={false} />
      <AuthModalProvider>
        <BrowserRouter>
          <AuthModal />
          <Routes>
            <Route element={<AppLayout />}>
              {/* <Route path="/" element={<Home />} /> */}
              <Route index element={<Home />} />
              <Route path="articles" element={<ArticleList />} />
              <Route
                path="articles/:username/:slug"
                element={<ArticleDetail />}
              />
              <Route path="jobs" element={<TechJobsList />} />
              <Route path="jobs/:jobId" element={<TechJobDetail />} />
              <Route path="events" element={<TechEventList />} />
              <Route path="events/:eventId" element={<TechEventDetail />} />
              <Route path="tools" element={<TechToolList />} />
              <Route path="tools/:toolId" element={<TechToolDetail />} />
              <Route path="resources" element={<ResourceList />} />
              <Route
                path="resources/:resourceId"
                element={<ResourceDetail />}
              />
              <Route path="categories">
                <Route index element={<CategoryList />} />
                <Route path=":categorySlug" element={<CategoryDetail />} />
                {/* <Route path=":categorySlug/articles" element={<ArticleList />} />
              <Route path=":categorySlug/articles/:articleSlug" element={<ArticleDetail />} /> */}
              </Route>
              <Route path="about" element={<About />} />
              <Route path="contact" element={<Contact />} />
              <Route path="newsletter/unsubscribe" element={<Unsubscribe />} />
              <Route path="login" element={<Login />} />
              <Route path="logout" element={<Logout />} />
              <Route path="register" element={<Register />} />
              <Route path="profile/:username" element={<ProfileDetail />} />
              <Route path="verify-email" element={<VerifyEmail />} />
              <Route
                path="auth/google/register/callback"
                element={<GoogleRegisterCallback />}
              />
              <Route
                path="auth/google/login/callback"
                element={<GoogleLoginCallback />}
              />
              <Route path="reset-password" element={<ResetPassword />} />
              <Route
                path="reset-password-success"
                element={<ResetPasswordSuccess />}
              />
              <Route path="docs" element={<Docs />} />
              <Route path="account-disabled" element={<AccountDisabled />} />
            </Route>

            <Route
              element={
                <ProtectedRoute>
                  <AppLayout />
                </ProtectedRoute>
              }
            >
              <Route path="new" element={<Liveblock />} />
              <Route path="account" element={<AccountDetail />} />
              <Route path="notifications" element={<NotificationList />} />
              <Route path="change-password" element={<ChangePassword />} />
              <Route path="payment/status" element={<PaymentStatus />} />
              <Route path="admin" element={<AdminDashboard />} />
            </Route>

            <Route path="coming-soon" element={<ComingSoon />} />
            <Route path="campuskart" element={<CampusKart />} />
            {/* Catch-all route for 404 errors */}
            <Route path="*" element={<PageNotFound />} />
          </Routes>
        </BrowserRouter>
      </AuthModalProvider>
      <Toaster
        position="top-right"
        toastOptions={{
          className: 'dark:!bg-dark dark:!text-white',
          style: {
            padding: '16px 24px',
            fontSize: '16px',
            maxWidth: '500px',
          },
        }}
      />
    </QueryClientProvider>
  );
}

export default App;
