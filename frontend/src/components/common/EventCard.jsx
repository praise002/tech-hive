import { MdOutlineDateRange } from 'react-icons/md';
import { HiOutlineLocationMarker } from 'react-icons/hi';
import { RiMapPinRangeLine } from 'react-icons/ri';
import PropTypes from 'prop-types';
import Button from './Button';
import Text from './Text';
import { Link } from 'react-router-dom';

function EventCard({ event }) {
  return (
    <div className="p-6 rounded-lg border border-gray dark:border-gray-700 shadow-lg h-full flex flex-col">
      <div className="flex-grow space-y-2">
        {/* Event Title */}
        <Text
          variant="h4"
          size="xl"
          bold={false}
          className="font-semibold text-gray-900 dark:text-custom-white"
        >
          {event.title}
        </Text>

        <div className="text-secondary text-sm">{event.organizer}</div>
        <div className="text-sm text-primary dark:text-custom-white space-y-2">
          {/* Date */}
          <div className="flex gap-2 items-center">
            <div>
              <MdOutlineDateRange className="w-5 h-5 md:w-7 md:h-7" />
            </div>
            <p>{event.date}</p>
          </div>

          {/* Location */}
          <div className="flex gap-2 items-center">
            <div>
              <HiOutlineLocationMarker className="w-5 h-5 md:w-7 md:h-7" />
            </div>
            <p>{event.location}</p>
          </div>

          {/* Virtual or Physical */}
          <div className="flex gap-2 items-center">
            <div>
              <RiMapPinRangeLine className="w-5 h-5 md:w-7 md:h-7" />
            </div>
            <p>{event.type}</p>
          </div>
        </div>
      </div>

      <div className="space-y-2 mt-2">
        {/* View Details Button */}
        <Button variant="outline" className="font-medium">
          <Link to="/events/a">View Details</Link>
        </Button>

        {/* Posted Time */}

        <div className="text-secondary text-xs">
          Posted {event.lastPosted} ago
        </div>
      </div>
    </div>
  );
}

EventCard.propTypes = {
  event: PropTypes.shape({
    title: PropTypes.string.isRequired,
    organizer: PropTypes.string.isRequired,
    date: PropTypes.string.isRequired,
    location: PropTypes.string.isRequired,
    type: PropTypes.string.isRequired,
    lastPosted: PropTypes.string.isRequired,
  }).isRequired,
};

export default EventCard;
