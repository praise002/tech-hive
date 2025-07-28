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
        alt={resource.resourceName}
        src={resource.resourceImage}
        className="flex-shrink-0"
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
              {resource.resourceName}
            </Text>
            <p className="text-xs text-secondary">{resource.resourceType}</p>
          </div>

          <Description>{resource.resourceDescription}</Description>

          <Tags tags={resource.resourceCategories} />
        </div>

        <div className="space-y-2">
          <Button variant="outline">
            <Link
              to="/resources/a"
              aria-label={`View details for ${resource.resourceName} (${resource.resourceType})`}
            >
              View details
            </Link>
          </Button>
          <div className="text-xs text-secondary">
            Posted {resource.timePosted}
          </div>
        </div>
      </div>
    </article>
  );
}

export default ResourceCard;
