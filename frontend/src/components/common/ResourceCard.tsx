import { ResourceCardProps } from '../../types/types';
import Button from './Button';
import Description from './Description';
import Image from './Image';
import Tags from './Tags';
import Text from './Text';
import { Link } from 'react-router-dom';

function ResourceCard({ resource }: ResourceCardProps) {
  return (
    <article className="relative overflow-hidden rounded-lg shadow-lg h-full flex flex-col">
      <Image
        alt={resource.name}
        src="/assets/resources/github-learning-lab.png"
        className="flex-shrink-0 h-48 w-full object-cover"
      />

      <div className="flex flex-col justify-between flex-grow p-5 border-l border-r border-b border-gray dark:border-gray-700 rounded-bl-lg rounded-br-lg overflow-hidden">
        <div className="space-y-2">
          <div>
            <Text
              variant="h4"
              size="xl"
              bold={false}
              className="font-semibold dark:text-custom-white"
            >
              {resource.name}
            </Text>
            {/* <p className="text-xs text-secondary">{resource.resourceType}</p> */}
          </div>

          <Description>{resource.body}</Description>

          <Tags tags={[{ id: resource.category, name: resource.category }]} />
        </div>

        <div className="space-y-2">
          <Button variant="outline">
            <Link
              to={`/resources/${resource.id}`}
              aria-label={`View details for ${resource.name}`}
            >
              View details
            </Link>
          </Button>
          <div className="text-xs text-secondary">
            Posted recently
            {/* Posted {resource.created_at} */}
          </div>
        </div>
      </div>
    </article>
  );
}

export default ResourceCard;
