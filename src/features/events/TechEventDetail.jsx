import Rectangle from '../../components/common/Rectangle';
import SocialLinks from '../../components/common/SocialLinks';
import Text from '../../components/common/Text';
import CategoryBar from '../../components/sections/CategoryBar';
import Subscribe from '../../components/sections/Subscribe';

function TechEventDetail() {
  return (
    <>
    <CategoryBar />
      <div className="flex flex-col md:flex-row gap-8 px-4 md:px-10 py-8">
        {/* Left Column: Social Links */}
        <div className="hidden md:block px-10 mt-70">
          <SocialLinks visible={false} />
        </div>

        {/* Right Column: Content */}
        <div className="p-2 w-full md:w-3/4 mt-20 md:mt-10 border border-[#C1C8C7]">
          <div>
            <Text
              variant="h3"
              size="xl"
              bold={false}
              className="font-semibold mb-2"
            >
              Africa Fintech Summit 2024
            </Text>
            <div className="text-[#889392] text-sm">Africa Fintech Summit</div>
          </div>
          <div className="space-y-8 text-[#262A2A]">
            {/* Description */}
            <div>
              <Text
                variant="h5"
                size="lg"
                bold={false}
                className="font-semibold mt-4"
              >
                Event Description
              </Text>
              <p className="text-base md:text-lg leading-relaxed">
                The Africa Fintech Summit 2024 is a premier event bringing
                together innovators, investors, and leaders shaping the fintech
                industry across the African continent.
              </p>
            </div>

            {/* Dates */}
            <div>
              <Text
                variant="h5"
                size="lg"
                bold={false}
                className="font-semibold mb-2"
              >
                Dates
              </Text>
              <ul className="list-disc pl-6 space-y-2 text-base md:text-lg leading-relaxed">
                <li>24–25 November 2024</li>
              </ul>
            </div>

            {/* Location */}
            <div>
              <Text
                variant="h5"
                size="lg"
                bold={false}
                className="font-semibold mb-2"
              >
                Location
              </Text>
              <ul className="list-disc pl-6 space-y-2 text-base md:text-lg leading-relaxed">
                <li>Cape Town, South Africa (In-person event)</li>
              </ul>
            </div>

            {/* Agenda */}
            <div>
              <Text
                variant="h5"
                size="lg"
                bold={false}
                className="font-semibold mb-2"
              >
                Agenda
              </Text>
              <ul className="list-disc pl-6 space-y-2 text-base md:text-lg leading-relaxed">
                <li>
                  Day 1: Keynote speeches, panel discussions, and networking
                  sessions.
                </li>
                <li>
                  Day 2: Workshops, product showcases, and startup pitch
                  competitions.
                </li>
              </ul>
            </div>

            {/* Tickets */}
            <div>
              <Text
                variant="h5"
                size="lg"
                bold={false}
                className="font-semibold mb-2"
              >
                Tickets
              </Text>
              <div className="flex gap-2 items-center text-base md:text-lg">
                <img src="/src/assets/icons/solar_link-bold.png" alt="" />
                <a
                  href="https://www.techgiant.inc/positions"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  https://www.techgiant.inc/positions
                </a>
              </div>
            </div>
          </div>
          <div className="text-[#889392] text-sm my-4">
            Posted 1 hour ago
          </div>
        </div>

        {/* Mobile social link */}
        <div className="block md:hidden text-center">
          <SocialLinks visible={false} />
        </div>
      </div>

      <Rectangle />
      <Subscribe />
    </>
  );
}

export default TechEventDetail;
