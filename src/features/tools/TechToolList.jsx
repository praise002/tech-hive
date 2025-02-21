import Button from '../../components/common/Button';
import Text from '../../components/common/Text';
import ToolCard from '../../components/common/ToolCard';
import { tools } from '../../data/tools';

function TechToolList() {
  return (
    <div className="pt-20 lg:pt-20 max-w-7xl mx-auto px-4 lg:px-8 mb-4">
      <div className="my-4">
        <Text variant="h3" size="xl" className="sm:2xl dark:text-custom-white">
          All Tools
        </Text>
        <div className="w-[20px]">
          <hr className="border-b-2 border-red" />
        </div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 2xl:grid-cols-4 gap-4 h-full">
        {tools.map((tool) => (
          <ToolCard key={tool.id} tool={tool} />
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

export default TechToolList;
