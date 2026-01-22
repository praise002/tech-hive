import { useParams } from 'react-router-dom';

import Rectangle from '../../components/common/Rectangle';
import Articles from '../../components/sections/Articles';
import CategoryBar from '../../components/sections/CategoryBar';
import ResourceSpotlight from '../../components/sections/ResourceSpotlight';
import Subscribe from '../../components/sections/Subscribe';
import TechEvents from '../../components/sections/TechEvents';
import TechJobs from '../../components/sections/TechJobs';
import TechTool from '../../components/sections/TechTool';
import TrendingArticles from '../../components/sections/TrendingArticles';
import { useCategoryDetail } from '../../hooks/useContent';
import Spinner from '../../components/common/Spinner';
import Text from '../../components/common/Text';

function CategoryDetail() {
  const { categorySlug } = useParams<{ categorySlug: string }>();
  const { category, isPending, isError, error } = useCategoryDetail(
    categorySlug!
  );

  if (isPending) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Spinner />
      </div>
    );
  }

  if (isError || !category) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center text-red-500">
          {error?.message || 'Category not found'}
        </div>
      </div>
    );
  }

  return (
    <>
      <CategoryBar />
      <div className="pt-20 lg:pt-10 max-w-7xl mx-auto px-4 lg:px-8">
        <Text variant="h1" size="2xl" className="dark:text-custom-white">
          {category.name}
        </Text>
        <Text
          variant="p"
          size="base"
          className="text-gray-600 dark:text-gray-400 mt-2"
        >
          {category.desc}
        </Text>
      </div>
      <TrendingArticles category={category.id} />
      <Articles category={category.id} />
      <TechJobs category={category.id} />
      <TechEvents category={category.id} />
      <TechTool category={category.id} />
      <ResourceSpotlight category={category.id} />
      <Rectangle />
      <Subscribe />
    </>
  );
}

export default CategoryDetail;
