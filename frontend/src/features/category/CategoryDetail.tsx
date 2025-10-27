import Rectangle from '../../components/common/Rectangle';
import Articles from '../../components/sections/Articles';

import CategoryBar from '../../components/sections/CategoryBar';
import ResourceSpotlight from '../../components/sections/ResourceSpotlight';
import Subscribe from '../../components/sections/Subscribe';
import TechEvents from '../../components/sections/TechEvents';
import TechJobs from '../../components/sections/TechJobs';
import TechTool from '../../components/sections/TechTool';
import TrendingArticles from '../../components/sections/TrendingArticles';

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
