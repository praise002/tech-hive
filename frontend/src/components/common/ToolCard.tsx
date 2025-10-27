import Image from './Image';
import Tags from './Tags';
import Text from './Text';
import Button from './Button';
import { ToolCardProps } from '../../types/types';

function ToolCard({ tool }: ToolCardProps) {
  return (
    <article className="relative overflow-hidden rounded-lg shadow-lg h-full flex flex-col">
      <Image
        alt={tool.toolName}
        src={tool.toolImage}
        className="flex-shrink-0"
      />

      <div className="flex flex-col justify-between flex-grow p-5 border-l border-r border-b border-gray dark:border-gray-700 rounded-bl-lg rounded-br-lg overflow-hidden">
        <div className="space-y-2">
          <Text
            variant="h4"
            size="xl"
            bold={false}
            className="font-semibold dark:text-custom-white"
          >
            {tool.toolName}
          </Text>
          <div className="text-sm md:text-base text-primary dark:text-custom-white">
            {tool.toolDescription}
          </div>
          <Tags tags={tool.toolCategories} />
        </div>

        <div className="mt-2">
          <Button className="text-xs w-auto" variant="outline">
            <a
              href={tool.link}
              target="_blank"
              rel="noopener noreferrer"
              aria-label={`Learn more about ${tool.toolName}: ${tool.callToAction}`}
            >
              {tool.callToAction}
            </a>
          </Button>
        </div>
      </div>
    </article>
  );
}

export default ToolCard;
