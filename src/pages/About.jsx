import Image from '../components/common/Image';
import Text from '../components/common/Text';
import SocialLinks from '../components/common/SocialLinks';
import Subscribe from '../components/sections/Subscribe';
import Rectangle from '../components/common/Rectangle';

function About() {
  return (
    <>
      <div className="flex flex-col md:flex-row gap-8 px-4 md:px-10 py-8">
        {/* Left Column: Social Links */}
        <div className="hidden md:block px-10 mt-70">
          <SocialLinks visible={false} />
        </div>

        {/* Right Column: Content */}
        <div className="w-full md:w-3/4 space-y-8 mt-20 md:mt-30 rounded-tl-lg rounded-tr-lg overflow-hidden">
          {/* Image */}

          <Image
            src="/src/assets/about.png"
            alt="About Tech Hive"
            className="w-full h-auto shadow-md"
          />

          {/* Welcome Section */}
          <div>
            <Text variant="h2" size="2xl" className="font-bold mb-4">
              Welcome to Tech Hive
            </Text>
            <p className="text-base md:text-lg leading-relaxed">
              At Tech Hive, we are passionate about everything tech. Whether
              you’re a budding developer, a seasoned professional, or a tech
              enthusiast exploring the latest innovations, our platform is your
              ultimate destination for insights, resources, and opportunities in
              the tech world.
            </p>
          </div>

          {/* Mission Section */}
          <div>
            <Text
              variant="h3"
              size="xl"
              bold={false}
              className="font-semibold mb-2"
            >
              Our Mission
            </Text>
            <p className="text-base md:text-lg leading-relaxed">
              To inspire and empower the global tech community by delivering
              high-quality content, tools, and resources that fuel innovation
              and drive progress.
            </p>
          </div>

          {/* Offer Section */}
          <div>
            <Text
              variant="h3"
              size="xl"
              bold={false}
              className="font-semibold mb-2"
            >
              What We Offer
            </Text>
            <ul className="list-disc pl-6 space-y-2 text-base md:text-lg leading-relaxed">
              <li>
                <span className="font-bold">Featured Tech Tools:</span> Discover
                innovative tools and software that can transform the way you
                work and create.
              </li>
              <li>
                <span className="font-bold">Tech Jobs:</span> Explore exciting
                career opportunities and connect with top companies shaping the
                future.
              </li>
              <li>
                <span className="font-bold">Tech Articles:</span> Dive into
                in-depth analyses, tutorials, and stories covering the latest
                trends and breakthroughs in technology.
              </li>
              <li>
                <span className="font-bold">Resource Spotlight:</span> Access
                curated resources to help you learn, grow, and stay ahead in the
                tech industry.
              </li>
            </ul>
          </div>

          {/* Why Section */}
          <div>
            <Text
              variant="h3"
              size="xl"
              bold={false}
              className="font-semibold mb-2"
            >
              Why Tech Hive?
            </Text>
            <p className="text-base md:text-lg leading-relaxed">
              Tech Hive is more than just a blog; it’s a thriving hub for tech
              enthusiasts and professionals. We’re dedicated to fostering a
              community where knowledge meets opportunity and ideas come to
              life.
            </p>
          </div>

          {/* Join the Buzz Section */}
          <div>
            <Text
              variant="h3"
              size="xl"
              bold={false}
              className="font-semibold mb-2"
            >
              Join the Buzz
            </Text>
            <p className="text-base md:text-lg leading-relaxed">
              Stay updated with the latest in tech by following us on our
              journey. Let’s shape the future of technology together!
            </p>
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

export default About;
