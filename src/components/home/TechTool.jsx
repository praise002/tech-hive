import Text from '../common/Text';
import { homePageTechTools } from '../../data/tools';
import ToolCard from '../common/ToolCard';
import Button from '../common/Button';

function TechTool() {
  return (
    <div>
      <div className="my-4">
        <Text variant="h3" size="xl" className="sm:2xl">
          Featured Tech Tool
        </Text>
        <div className="w-[20px]">
          <hr className="border-b-2 border-[#a32816]" />
        </div>
      </div>

      <div className="flex flex-col gap-y-2">
        {homePageTechTools.map((tool, index) => (
          <ToolCard key={index} tool={tool} />
        ))}
      </div>

      <Button className='my-4'>Explore More Tools &rarr;</Button>
    </div>
  );
}

export default TechTool;
