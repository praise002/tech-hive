import HeroSection from '../components/sections/HeroSection';
import Subscribe from '../components/sections/Subscribe';
import TechDashboard from '../components/sections/TechDashboard';
import TrendingArticles from '../components/sections/TrendingArticles';

function Home() {
  return (
    <>
      <HeroSection />
      <TrendingArticles />
      <TechDashboard />
      <Subscribe />
    </>
  );
}

export default Home;
