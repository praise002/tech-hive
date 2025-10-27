// import Button from '../common/Button';
import { Link } from 'react-router-dom';

import ResourceCard from '../common/ResourceCard';
import Text from '../common/Text';
import { displayedResources } from '../../data/resources';

function ResourceSpotlight() {
  return (
    <section
      className="mt-20 lg:mt-4 max-w-7xl mx-auto px-4 lg:px-8 mb-4"
      aria-label="Tech resources"
    >
      <div className="flex justify-between items-center">
        <div className="my-4">
          <Text
            variant="h3"
            size="xl"
            className="sm:2xl dark:text-custom-white"
          >
            Resource Spotlight
          </Text>
          <div className="w-[20px]" aria-hidden="true">
            <hr className="border-b-2 border-red" />
          </div>
        </div>
        <div>
          <Link
            to="/resources"
            className="cursor-pointer text-secondary hover:text-red transition-colors"
            aria-label="See all tech resources"
          >
            See all
          </Link>
        </div>
      </div>
      <ul className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 h-full">
        {displayedResources.map((resource) => (
          <li key={resource.id}>
            <ResourceCard resource={resource} />
          </li>
        ))}
      </ul>

      {/* <Button>Explore More Resources &rarr;</Button> */}
    </section>
  );
}

export default ResourceSpotlight;
