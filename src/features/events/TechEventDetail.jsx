import Text from '../../components/common/Text';

function TechEventDetail() {
  return (
    <div className="border-[#C1C8C7]">
      <div>
        <Text
          variant="h3"
          size="xl"
          bold={false}
          className="font-semibold text-gray-900 mb-2"
        >
          Africa Fintech Summit 2024
        </Text>
        <div className="text-[#889392] text-sm">Africa Fintech Summit</div>
      </div>
      <div>
        {/* Description */}
        <div>
          <Text
            variant="h5"
            size="lg"
            bold={false}
            className="font-semibold text-gray-900 mb-2"
          >
            Event Description
          </Text>
          <p className="text-[#262A2A]">
            The Africa Fintech Summit 2024 is a premier event bringing together
            innovators, investors, and leaders shaping the fintech industry
            across the African continent.
          </p>
        </div>

        {/* Dates */}
        <ul>
          <Text
            variant="h5"
            size="lg"
            bold={false}
            className="font-semibold text-gray-900 mb-2"
          >
            Dates
          </Text>
          <li>24–25 November 2024</li>
        </ul>

        {/* Location */}
        <ul>
          <Text
            variant="h5"
            size="lg"
            bold={false}
            className="font-semibold text-gray-900 mb-2"
          >
            Location
          </Text>
          <li>Cape Town, South Africa (In-person event)</li>
        </ul>

        {/* Agenda */}
        <ul>
          <Text
            variant="h5"
            size="lg"
            bold={false}
            className="font-semibold text-gray-900 mb-2"
          >
            Agenda
          </Text>
          <li>
            Day 1: Keynote speeches, panel discussions, and networking sessions.
          </li>
          <li>
            Day 2: Workshops, product showcases, and startup pitch competitions.
          </li>
        </ul>

        {/* Tickets */}
        <div>
          <Text
            variant="h5"
            size="lg"
            bold={false}
            className="font-semibold text-gray-900 mb-2"
          >
            Tickets
          </Text>
          <div>
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
      <div className="text-[#889392] text-sm">Posted 1 hour ago</div>
    </div>
  );
}

export default TechEventDetail;
