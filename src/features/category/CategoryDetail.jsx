import Rectangle from '../../components/common/Rectangle';
import Articles from './components/Articles';

import CategoryBar from '../../components/sections/CategoryBar';
import ResourceSpotlight from './components/ResourceSpotlight';
import Subscribe from '../../components/sections/Subscribe';
import TechEvents from './components/TechEvents';
import TechJobs from './components/TechJobs';
import TechTool from './components/TechTool';
import TrendingArticles from './components/TrendingArticles';

function CategoryDetail() {
  return (
    <>
      <CategoryBar />
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

export default CategoryDetail;
