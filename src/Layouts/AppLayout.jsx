import { Outlet } from 'react-router-dom';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';

function AppLayout() {
  return (
    <div>
      <Navbar />
      <main>
        <Outlet /> {/* This is where child routes will be rendered */}
      </main>
      <Footer />
    </div>
  );
}

export default AppLayout;
