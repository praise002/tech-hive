import { homepageResources } from '../../data/resources';
import Button from '../common/Button';
import ResourceCard from '../common/ResourceCard';
import Text from '../common/Text';

function ResourceSpotlight() {
  return (
    <div>
      <div className="my-4">
        <Text variant="h3" size="xl" className="sm:2xl">
          Resource Spotlight
        </Text>
        <div className="w-[20px]">
          <hr className="border-b-2 border-[#a32816]" />
        </div>
      </div>
      <div className="flex flex-col gap-y-2">
        {homepageResources.map((resource, index) => (
          <ResourceCard key={index} resource={resource} />
        ))}
      </div>

      <Button className='my-4'>Explore More Resources &rarr;</Button>
    </div>
  );
}

export default ResourceSpotlight;
