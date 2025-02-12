import PropTypes from 'prop-types';
import Button from './Button';
import Description from './Description';
import Image from './Image';
import Tags from './Tags';
import Text from './Text';

function ResourceCard({ resource }) {
  return (
    <div className="relative overflow-hidden rounded-lg shadow-lg h-full flex flex-col">
      <Image
        alt={resource.resourceName}
        src={resource.resourceImage}
        className="flex-shrink-0"
      />

      <div className="flex flex-col justify-between flex-grow p-5 border-l border-r border-b border-[#C1C8C7] rounded-bl-lg rounded-br-lg overflow-hidden">
        <div className="space-y-2">
          <div>
            <Text variant="h4" size="xl" bold={false} className="font-semibold">
              {resource.resourceName}
            </Text>
            <p className="text-xs text-[#889392]">{resource.resourceType}</p>
          </div>

          <Description>{resource.resourceDescription}</Description>

          <Tags tags={resource.resourceCategories} />
        </div>

        <div className="space-y-2">
          <Button variant="outline">View details</Button>
          <div className="text-xs text-[#889392]">
            Posted {resource.timePosted}
          </div>
        </div>
      </div>
    </div>
  );
}

ResourceCard.propTypes = {
  resource: PropTypes.shape({
    resourceName: PropTypes.string.isRequired,
    resourceImage: PropTypes.string.isRequired,
    resourceType: PropTypes.string.isRequired,
    resourceDescription: PropTypes.string.isRequired,
    resourceCategories: PropTypes.arrayOf(
      PropTypes.shape({
        name: PropTypes.string.isRequired,
        color: PropTypes.string.isRequired,
      })
    ).isRequired,
    timePosted: PropTypes.string.isRequired,
    
  }).isRequired,
};

export default ResourceCard;
