import Button from '../../components/common/Button';
import ResourceCard from '../../components/common/ResourceCard';
import Text from '../../components/common/Text';
import { resources } from '../../data/resources';

function ResourceList() {
  return (
    <div className="mt-20 lg:mt-20 max-w-7xl mx-auto px-4 lg:px-8 mb-4">
      <div className="my-4">
        <Text variant="h3" size="2xl" className="sm:xl">
          All Resources
        </Text>
        <div className="w-[20px]">
          <hr className="border-b-2 border-[#a32816]" />
        </div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 2xl:grid-cols-4 gap-4 h-full">
        {resources.map((resource) => (
          <ResourceCard key={resource.id} resource={resource} />
        ))}
      </div>

      {/* Static Pagination */}
      <div className="max-w-7xl mx-auto mt-8 flex items-center justify-center">
        <div className="flex items-center space-x-2">
          <Button variant="primary">Previous</Button>

          <span className="text-gray-600">Page 1 of 5</span>
          <Button variant="primary">Next</Button>
        </div>
      </div>
    </div>
  );
}

export default ResourceList;
