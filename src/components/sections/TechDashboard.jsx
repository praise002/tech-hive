import TrendingArticles from '../home/TrendingArticles';
import TechJobs from '../home/TechJobs';
import TechTool from '../home/TechTool';
import TechEvents from '../home/TechEvents';
import ResourceSpotlight from '../home/ResourceSpotlight';

function TechDashboard() {
  return (
    <div className="mt-20 lg:mt-4 max-w-7xl mx-auto px-4 lg:px-8 mb-4">
      <div className="xl:grid gap-4 hidden xl:grid-cols-3">
        <div>
          <TechJobs />
          <TechEvents />
        </div>
        <TrendingArticles />
        <div>
          <TechTool />
          <ResourceSpotlight />
        </div>
      </div>
    </div>
  );
}

export default TechDashboard;
