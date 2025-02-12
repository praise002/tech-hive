import { homePageEvents } from '../../data/events';
import Button from '../common/Button';
import EventCard from '../common/EventCard';
import Text from '../common/Text';

function TechEvents() {
  return (
    <div>
      <div className="my-4">
        <Text variant="h3" size="xl" className="sm:2xl">
          Tech Events
        </Text>
        <div className="w-[20px]">
          <hr className="border-b-2 border-[#a32816]" />
        </div>
      </div>

      <div className="flex flex-col gap-y-2">
        {homePageEvents.map((event, index) => (
          <EventCard key={index} event={event} />
        ))}
      </div>
      <Button className="my-4">Explore More Events &rarr;</Button>
    </div>
  );
}

export default TechEvents;
