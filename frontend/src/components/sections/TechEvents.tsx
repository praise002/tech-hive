import { Link } from 'react-router-dom';

import EventCard from '../common/EventCard';
import Text from '../common/Text';
import { displayedEvents } from '../../data/events';

function TechEvents() {
  return (
    <section
      className="mt-20 lg:mt-4  mx-auto px-4 lg:px-8 mb-4"
      aria-label="Tech events"
    >
      {/* max-w-7xl */}
      <div className="flex justify-between items-center">
        <div className="my-4">
          <Text
            variant="h3"
            size="xl"
            className="sm:2xl dark:text-custom-white"
          >
            Tech Events
          </Text>
          <div className="w-[20px]" aria-hidden="true">
            <hr className="border-b-2 border-red" />
          </div>
        </div>
        <div>
          <Link
            to="/events"
            className="cursor-pointer text-secondary hover:text-red transition-colors"
            aria-label="See all tech events"
          >
            See all
          </Link>
        </div>
      </div>

      <ul className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 h-full">
        {/* <div className="flex flex-col gap-y-2"> */}
        {displayedEvents.map((event) => (
          <li key={event.id}>
            <EventCard event={event} />
          </li>
        ))}
      </ul>
      {/* <Button>Explore More Jobs &rarr;</Button> */}
    </section>
  );
}

export default TechEvents;
