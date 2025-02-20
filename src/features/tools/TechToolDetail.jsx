import Image from '../../components/common/Image';
import Rectangle from '../../components/common/Rectangle';
import SocialLinks from '../../components/common/SocialLinks';
import Text from '../../components/common/Text';
import CategoryBar from '../../components/sections/CategoryBar';
import Subscribe from '../../components/sections/Subscribe';

function TechToolDetail() {
  return (
    <>
      <CategoryBar />
      <div className="flex flex-col md:flex-row gap-8 px-4 md:px-10 py-8">
        {/* Left Column: Social Links */}
        <div className="hidden md:block px-10 mt-70">
          <SocialLinks visible={false} />
        </div>

        {/* Right Column: Content */}
        <div className="w-full md:w-3/4 mt-20 md:mt-10 border border-gray rounded-tl-lg rounded-tr-lg overflow-hidden">
          <Image
            alt="Figma"
            src="/src/assets/tech-tool/figma.png"
            className="w-full h-auto shadow-md"
          />
          <div className="space-y-8 px-2 text-color-text-primary">
            <Text
              variant="h3"
              size="xl"
              bold={false}
              className="font-semibold mt-4"
            >
              What is Figma?
            </Text>

            {/* Description */}
            <div>
              <Text
                variant="h5"
                size="lg"
                bold={false}
                className="font-semibold mb-2"
              >
                Software Description
              </Text>
              <p className="text-base md:text-lg leading-relaxed">
                Figma is a cloud-based design and prototyping tool used for
                creating user interfaces, wireframes, and collaborative design
                projects. It&apos;s a favorite among UI/UX designers for its
                intuitive interface and real-time collaboration features.
              </p>
            </div>

            {/* Key Features */}
            <div>
              <Text
                variant="h5"
                size="lg"
                bold={false}
                className="font-semibold mb-2"
              >
                Key Features
              </Text>
              <ul className="list-disc pl-6 space-y-2 text-base md:text-lg leading-relaxed">
                <li>Design and prototype in one tool.</li>
                <li>Share designs and get feedback instantly.</li>
                <li>Works on any platform with an internet connection.</li>
                <li>Extensive library of plugins to enhance productivity.</li>
              </ul>
            </div>

            {/* Use Cases */}
            <div>
              <Text
                variant="h5"
                size="lg"
                bold={false}
                className="font-semibold mb-2"
              >
                Use Cases
              </Text>
              <ul className="list-disc pl-6 space-y-2 text-base md:text-lg leading-relaxed">
                <li>User interface design for apps and websites.</li>
                <li>
                  Creating interactive prototypes for client presentations.
                </li>
                <li>Team collaboration on design projects.</li>
              </ul>
            </div>

            {/* How to Access */}
            <div>
              <Text
                variant="h5"
                size="lg"
                bold={false}
                className="font-semibold mb-2"
              >
                How to Access
              </Text>
              <div className="flex gap-2 items-center text-base md:text-lg">
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
          <div className="px-2 text-color-text-secondary text-sm my-4">
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

export default TechToolDetail;
