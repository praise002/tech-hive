import Rectangle from '../components/common/Rectangle';
import HeroSection from '../components/sections/HeroSection';
import Subscribe from '../components/sections/Subscribe';
import Articles from '../components/sections/Articles';
import ResourceSpotlight from '../components/sections/ResourceSpotlight';
import TechEvents from '../components/sections/TechEvents';
import TechJobs from '../components/sections/TechJobs';
import TechTool from '../components/sections/TechTool';
import TrendingArticles from '../components/sections/TrendingArticles';

function Home() {
  return (
    <div>
      <HeroSection />
      <TrendingArticles />
      <Articles />
      <TechJobs />
      <TechEvents />
      <TechTool />
      <ResourceSpotlight />
      <Rectangle />
      <Subscribe />
    </div>
  );
}

export default Home;
