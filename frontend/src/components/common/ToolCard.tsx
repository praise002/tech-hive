import Image from './Image';
import Tags from './Tags';
import Text from './Text';
import { ToolCardProps } from '../../types/types';

function ToolCard({ tool }: ToolCardProps) {
  return (
    <article className="relative overflow-hidden rounded-lg shadow-lg h-full flex flex-col">
      <Image
        alt={tool.name}
        src="/assets/tech-tool/figma.png"
        className="flex-shrink-0 h-48 w-full object-cover"
      />

      <div className="flex flex-col justify-between flex-grow p-5 border-l border-r border-b border-gray dark:border-gray-700 rounded-bl-lg rounded-br-lg overflow-hidden">
        <div className="space-y-2">
          <Text
            variant="h4"
            size="xl"
            bold={false}
            className="font-semibold dark:text-custom-white"
          >
            {tool.name}
          </Text>
          <div className="text-sm md:text-base text-primary dark:text-custom-white">
            {tool.desc}
          </div>
          <Tags tags={[{ id: tool.category, name: tool.category }]} />
        </div>

        <div className="mt-4">
          <a
            href={tool.url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center justify-center px-4 py-2 border border-red text-red hover:bg-red-800 hover:text-white rounded-lg text-sm font-medium transition duration-300 w-full md:w-auto"
            aria-label={`Learn more about ${tool.name}: ${tool.call_to_action}`}
          >
            {tool.call_to_action}
          </a>
        </div>
      </div>
    </article>
  );
}

export default ToolCard;
