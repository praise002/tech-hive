import Image from '../../components/common/Image';
import Text from '../../components/common/Text';

function TechToolDetail() {
  return (
    <div className="border-[#C1C8C7]">
      <Image alt="Figma" src="/src/assets/tech-tool/figma.png" />
      <div>
        <Text
          variant="h3"
          size="lg"
          bold={false}
          className="font-semibold text-gray-900 mb-2"
        >
          What is Figma?
        </Text>

        {/* Description */}
        <div>
          <Text
            variant="h5"
            size="lg"
            bold={false}
            className="font-semibold text-gray-900 mb-2"
          >
            Software Description
          </Text>
          <p className="text-[#262A2A]">
            Figma is a cloud-based design and prototyping tool used for creating
            user interfaces, wireframes, and collaborative design projects. It's
            a favorite among UI/UX designers for its intuitive interface and
            real-time collaboration features.
          </p>
        </div>

        {/* Key Features */}
        <ul>
          <Text
            variant="h5"
            size="lg"
            bold={false}
            className="font-semibold text-gray-900 mb-2"
          >
            Key Features
          </Text>
          <li>Design and prototype in one tool.</li>
          <li>Share designs and get feedback instantly.</li>
          <li>Works on any platform with an internet connection.</li>
          <li>Extensive library of plugins to enhance productivity.</li>
        </ul>

        {/* Use Cases */}
        <ul>
          <Text
            variant="h5"
            size="lg"
            bold={false}
            className="font-semibold text-gray-900 mb-2"
          >
            Use Cases
          </Text>
          <li>User interface design for apps and websites.</li>
          <li>Creating interactive prototypes for client presentations.</li>
          <li>Team collaboration on design projects.</li>
        </ul>

        {/* How to Access */}
        <div>
          <Text
            variant="h5"
            size="lg"
            bold={false}
            className="font-semibold text-gray-900 mb-2"
          >
            How to Access
          </Text>
          <div>
            <img src="/src/assets/icons/solar_link-bold.png" alt="" />
            <a
              href="https://www.figma.com"
              target="_blank"
              rel="noopener noreferrer"
            >
              https://www.figma.com
            </a>
          </div>
        </div>
      </div>
      <div className="text-[#889392] text-sm">Posted 1 hour ago</div>
    </div>
  );
}

export default TechToolDetail;
