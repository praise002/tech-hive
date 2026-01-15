import { useParams } from 'react-router-dom';
import Rectangle from '../../components/common/Rectangle';
import SocialLinks from '../../components/common/SocialLinks';
import Text from '../../components/common/Text';
import CategoryBar from '../../components/sections/CategoryBar';
import Subscribe from '../../components/sections/Subscribe';
import { useEventDetail } from '../../hooks/useContent';
import Loader from '../../components/common/Loader';
import { formatDate } from '../../utils/utils';

function TechEventDetail() {
  const { id } = useParams<{ id: string }>();
  const { event, isPending, isError, error } = useEventDetail(id || '');

  if (isPending) {
    return (
      <div className="flex justify-center items-center h-screen">
        <Loader />
      </div>
    );
  }

  if (isError || !event) {
    return (
      <div className="text-center py-20 text-red-500">
        Error loading event: {error?.message}
      </div>
    );
  }

  return (
    <>
      <CategoryBar />
      <div className="flex flex-col md:flex-row gap-8 px-4 md:px-10 py-8">
        {/* Left Column: Social Links */}
        <div className="hidden md:block px-10 mt-70">
          <SocialLinks
            visible={false}
            title={event.title}
            sharemsg={`Join us at ${event.title}`}
            url={window.location.href}
          />
        </div>

        {/* Right Column: Content */}
        <div className="p-2 w-full md:w-3/4 mt-20 md:mt-10 border border-gray">
          <div>
            <Text
              variant="h3"
              size="xl"
              bold={false}
              className="font-semibold mb-2 dark:text-custom-white "
            >
              {event.title}
            </Text>
            <div className="text-secondary text-sm">{event.category.name}</div>
          </div>
          <div className="space-y-8 text-primary">
            {/* Description */}
            <div className="dark:text-custom-white">
              <Text
                variant="h5"
                size="lg"
                bold={false}
                className="font-semibold mt-4 dark:text-custom-white"
              >
                Event Description
              </Text>
              <div
                className="text-base md:text-lg leading-relaxed"
                dangerouslySetInnerHTML={{ __html: event.desc }}
              />
            </div>

            {/* Dates */}
            <div className="dark:text-custom-white">
              <Text
                variant="h5"
                size="lg"
                bold={false}
                className="font-semibold mb-2 dark:text-custom-white"
              >
                Dates
              </Text>
              <ul className="list-disc pl-6 space-y-2 text-base md:text-lg leading-relaxed">
                <li>
                  {formatDate(event.start_date)} - {formatDate(event.end_date)}
                </li>
              </ul>
            </div>

            {/* Location */}
            <div className="dark:text-custom-white">
              <Text
                variant="h5"
                size="lg"
                bold={false}
                className="font-semibold mb-2 dark:text-custom-white"
              >
                Location
              </Text>
              <ul className="list-disc pl-6 space-y-2 text-base md:text-lg leading-relaxed">
                <li>{event.location}</li>
              </ul>
            </div>

            {/* Agenda */}
            <div className="dark:text-custom-white">
              <Text
                variant="h5"
                size="lg"
                bold={false}
                className="font-semibold mb-2 dark:text-custom-white"
              >
                Agenda
              </Text>
              <div
                className="text-base md:text-lg leading-relaxed"
                dangerouslySetInnerHTML={{ __html: event.agenda }}
              />
            </div>

            {/* Tickets */}
            <div className="dark:text-custom-white">
              <Text
                variant="h5"
                size="lg"
                bold={false}
                className="font-semibold mb-2 dark:text-custom-white"
              >
                Tickets
              </Text>
              {event.ticket_url && (
                <div className="flex gap-2 items-center text-base md:text-lg">
                  <img
                    src="/assets/icons/solar_link-bold.png"
                    className="dark:invert"
                    alt=""
                  />
                  <a
                    href={event.ticket_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    aria-label={`Get tickets for ${event.title} (opens in new tab)`}
                  >
                    {event.ticket_url}
                  </a>
                </div>
              )}
            </div>
          </div>
          {/* <div className="text-secondary text-sm my-4">Posted 1 hour ago</div> */}
        </div>

        {/* Mobile social link */}
        <div className="block md:hidden text-center">
          <SocialLinks
            visible={false}
            title={event.title}
            sharemsg={`Join us at ${event.title}`}
            url={window.location.href}
          />
        </div>
      </div>

      <Rectangle />
      <Subscribe />
    </>
  );
}

export default TechEventDetail;
