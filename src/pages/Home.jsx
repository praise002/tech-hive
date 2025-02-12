import Rectangle from '../components/common/Rectangle';
import HeroSection from '../components/sections/HeroSection';
import Subscribe from '../components/sections/Subscribe';
import Articles from '../features/category/components/Articles';
import ResourceSpotlight from '../features/category/components/ResourceSpotlight';
import TechEvents from '../features/category/components/TechEvents';
import TechJobs from '../features/category/components/TechJobs';
import TechTool from '../features/category/components/TechTool';
import TrendingArticles from '../features/category/components/TrendingArticles';
// import TechDashboard from '../components/sections/TechDashboard';

function Home() {
  return (
    <>
      <HeroSection />
      {/* <TechDashboard /> */}
      <TrendingArticles />
      <Articles />
      <TechJobs />
      <TechEvents />
      <TechTool />
      <ResourceSpotlight />
      <Rectangle />
      <Subscribe />
    </>
  );
}

export default Home;
