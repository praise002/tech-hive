import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';

import About from './pages/About';
import AccountDetail from './features/profile/AccountDetail';
import AppLayout from './components/Layouts/AppLayout';
import ArticleDetail from './features/articles/ArticleDetail';
import ArticleList from './features/articles/ArticleList';
import CategoryDetail from './features/category/CategoryDetail';
import CategoryList from './features/category/CategoryList';
import Contact from './pages/Contact';
import Dashboard from './pages/Dashboard';
import Home from './pages/Home';
import Login from './features/auth/Login';
import PageNotFound from './pages/PageNotFound';
import ProfileDetail from './features/profile/ProfileDetail';
import Register from './features/auth/Register';
import TechEventList from './features/events/TechEventList';
import TechEventDetail from './features/events/TechEventDetail';

import TechJobDetail from './features/jobs/TechJobDetail';
import TechJobsList from './features/jobs/TechJobsList';
import TechToolDetail from './features/tools/TechToolDetail';
import TechToolList from './features/tools/TechToolList';

import ResourceList from './features/resource/ResourceList';
import ResourceDetail from './features/resource/ResourceDetail';
import ChangePassword from './features/auth/ChangePassword';
import ResetPassword from './features/auth/ResetPassword';
import ResetPasswordSuccess from './features/auth/ResetPaswordSuccess';
import { Toaster } from 'react-hot-toast';

import AdminDashboard from './features/admin/AdminDashboard';

import Liveblock from './features/articles/Liveblock';
import Docs from './features/articles/Docs';

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
      <BrowserRouter>
        <Routes>
          <Route element={<AppLayout />}>
            {/* <Route path="/" element={<Home />} /> */}
            <Route index element={<Home />} />
            <Route path="articles" element={<ArticleList />} />
            <Route path="articles/:articleSlug" element={<ArticleDetail />} />
            <Route path="jobs" element={<TechJobsList />} />
            <Route path="jobs/:jobSlug" element={<TechJobDetail />} />
            <Route path="events" element={<TechEventList />} />
            <Route path="events/:eventSlug" element={<TechEventDetail />} />
            <Route path="tools" element={<TechToolList />} />
            <Route path="tools/:toolSlug" element={<TechToolDetail />} />
            <Route path="resources" element={<ResourceList />} />
            <Route
              path="resources/:resourceSlug"
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
            <Route path="dashboard" element={<Dashboard />} />

            <Route path="new" element={<Liveblock />} />
            <Route path="profile" element={<ProfileDetail />} />

            <Route path="account" element={<AccountDetail />} />
            <Route path="login" element={<Login />} />
            <Route path="register" element={<Register />} />
            <Route path="change-password" element={<ChangePassword />} />
            <Route path="reset-password" element={<ResetPassword />} />
            <Route
              path="reset-password-success"
              element={<ResetPasswordSuccess />}
            />

            <Route path="admin" element={<AdminDashboard />} />
            <Route path="docs" element={<Docs />} />
          </Route>

          {/* Catch-all route for 404 errors */}
          <Route path="*" element={<PageNotFound />} />
        </Routes>
      </BrowserRouter>
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

// filtering - categories/slug/trending-articles, categories/slug/featured-tech-tool,
// categories/slug/job-in-tech
// categories/slug/articles, categories/resource-spotlight
// =?filter=trending, =?filter=resource-spotlight
