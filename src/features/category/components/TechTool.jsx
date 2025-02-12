// import Button from '../common/Button';
import { Link } from 'react-router-dom';
import { displayedTechTools } from '../../../data/tools.js';
import Text from '../../../components/common/Text.jsx';
import ToolCard from '../../../components/common/ToolCard.jsx';

function TechTool() {
  return (
    <div className="mt-20 lg:mt-4 max-w-7xl mx-auto px-4 lg:px-8 mb-4">
      <div className="flex justify-between items-center">
        <div className="my-4">
          <Text variant="h3" size="xl" className="sm:2xl">
            Featured Tech Tool
          </Text>
          <div className="w-[20px]">
            <hr className="border-b-2 border-[#a32816]" />
          </div>
        </div>
        <div>
          <Link
            to="tools"
            className="cursor-pointer text-[#889392] hover:text-[#a32816] transition-colors"
          >
            See all
          </Link>
        </div>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 h-full">
        {/* <div className="flex flex-col gap-y-2"> */}
        {displayedTechTools.map((tool, index) => (
          <ToolCard key={index} tool={tool} />
        ))}
      </div>

      {/* <Button>Explore More Tools &rarr;</Button> */}
    </div>
  );
}

export default TechTool;
