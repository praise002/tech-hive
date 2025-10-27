import Button from '../../components/common/Button';
import ResourceCard from '../../components/common/ResourceCard';
import Text from '../../components/common/Text';
import { resources } from '../../data/resources';

function ResourceList() {
  return (
    <div className="pt-20 lg:pt-20 max-w-7xl mx-auto px-4 lg:px-8 mb-4">
      <div className="my-4">
        <Text variant="h3" size="2xl" className="sm:xl dark:text-custom-white">
          All Resources
        </Text>
        <div className="w-[20px]" aria-hidden="true">
          <hr className="border-b-2 border-red" />
        </div>
      </div>
      <ul className="grid grid-cols-1 md:grid-cols-2 2xl:grid-cols-4 gap-4 h-full">
        {resources.map((resource) => (
          <li key={resource.id}>
            <ResourceCard resource={resource} />
          </li>
        ))}
      </ul>

      {/* Static Pagination */}
      <nav className="max-w-7xl mx-auto mt-8 flex items-center justify-center">
        <div className="flex items-center space-x-2">
          <Button variant="primary" aria-label="Go to previous page">
            Previous
          </Button>

          <span className="text-gray-600" aria-live="polite">
            Page 1 of 5
          </span>
          <Button variant="primary" aria-label="Go to next page">
            Next
          </Button>
        </div>
      </nav>
    </div>
  );
}

export default ResourceList;
