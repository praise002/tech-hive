import { Outlet } from 'react-router-dom';
import Navbar from './Navbar';
import Footer from './Footer';

function AppLayout() {
  return (
    <div className="font-inter dark:bg-dark min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-grow">
        <Outlet /> {/* This is where child routes will be rendered */}
      </main>
      <Footer />
    </div>
  );
}

export default AppLayout;
