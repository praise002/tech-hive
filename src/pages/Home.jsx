// import SocialLinks from '../components/common/SocialLinks';
// import CategoryBar from '../components/sections/CategoryBar';
import HeroSection from '../components/sections/HeroSection';
// import ResourceSpotlight from '../components/sections/ResourceSpotlight';
import Subscribe from '../components/sections/Subscribe';
import TechDashboard from '../components/sections/TechDashboard';
// import TechTool from '../components/sections/TechTool';

// import TrendingArticles from '../components/sections/TrendingArticles';

function Home() {
  return (
    <>
      {/* <CategoryBar /> */}
      <HeroSection />
      {/* <TrendingArticles /> */}
      {/* <TechTool /> */}
      {/* <ResourceSpotlight /> */}
      {/* <SocialLinks /> */}
      <TechDashboard />
      <Subscribe />
      <div className="m-5"></div>
    </>
  );
}

export default Home;
