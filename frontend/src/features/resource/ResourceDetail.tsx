import Image from '../../components/common/Image';
import Rectangle from '../../components/common/Rectangle';
import SocialLinks from '../../components/common/SocialLinks';
import Text from '../../components/common/Text';
import CategoryBar from '../../components/sections/CategoryBar';
import Subscribe from '../../components/sections/Subscribe';

function ResourceDetail() {
  return (
    <>
      <CategoryBar />
      <div className="flex flex-col md:flex-row gap-8 px-4 md:px-10 py-8">
        {/* Left Column: Social Links */}
        <div className="hidden md:block px-10 mt-70">
          <SocialLinks
            visible={false}
            title="Github Learning Lab"
            sharemsg="Check out this resource on Github Learning Lab"
            url={window.location.href}
          />
        </div>

        {/* Right Column: Content */}
        <div className="w-full md:w-3/4 mt-20 md:mt-10 border border-gray rounded-tl-lg rounded-tr-lg overflow-hidden">
          <Image
            alt="Github Learning Lab"
            src="/assets/resources/github-learning-lab.png"
            className="w-full h-auto shadow-md"
          />
          <div className="space-y-8 px-2 text-primary">
            <Text
              variant="h3"
              size="xl"
              bold={false}
              className="font-semibold mt-4 dark:text-custom-white"
            >
              Github Learning Lab
            </Text>

            {/* Description */}
            <div>
              <Text
                variant="h5"
                size="lg"
                bold={false}
                className="font-semibold mb-2 dark:text-custom-white"
              >
                Software Description
              </Text>
              <p className="text-base md:text-lg leading-relaxed dark:text-custom-white">
                GitHub Learning Lab is an educational platform offering
                interactive, project-based courses to improve your skills in
                software development, version control, and open-source
                collaboration.
              </p>
            </div>

            {/* Popular Courses */}
            <div>
              <Text
                variant="h5"
                size="lg"
                bold={false}
                className="font-semibold mb-2 dark:text-custom-white"
              >
                Popular Courses
              </Text>
              <ul className="dark:text-custom-white list-disc pl-6 space-y-2 text-base md:text-lg leading-relaxed">
                <li>Introduction to Git and GitHub.</li>
                <li>Building RESTful APIs.</li>
                <li>Works on any platform with an internet connection.</li>
                <li>Advanced topics in software development.</li>
              </ul>
            </div>

            {/* Why Learn Here? */}
            <div>
              <Text
                variant="h5"
                size="lg"
                bold={false}
                className="font-semibold mb-2 dark:text-custom-white"
              >
                Why Learn Here?
              </Text>
              <ul className="dark:text-custom-white list-disc pl-6 space-y-2 text-base md:text-lg leading-relaxed">
                <li>Hands-on exercises with real-world applications.</li>
                <li>
                  Earn certificates of completion to showcase your skills.
                </li>
                <li>Supportive community of learners and mentors.</li>
              </ul>
            </div>

            {/* How to Access */}
            <div>
              <Text
                variant="h5"
                size="lg"
                bold={false}
                className="font-semibold mb-2 dark:text-custom-white"
              >
                How to Access
              </Text>
              <div className="flex gap-2 items-center text-base md:text-lg dark:text-custom-white">
                <img
                  className="dark:invert"
                  src="/assets/icons/solar_link-bold.png"
                  alt=""
                />
                <a
                  href="https://www.github.com"
                  target="_blank"
                  rel="noopener noreferrer"
                  aria-label="Visit Github Learning Lab (opens in new tab)"
                >
                  https://www.github.com
                </a>
              </div>
            </div>
          </div>
          <div className="px-2 text-secondary text-sm my-4">
            Posted 1 hour ago
          </div>
        </div>

        {/* Mobile social link */}
        <div className="block md:hidden text-center">
          <SocialLinks
            visible={false}
            title="Github Learning Lab"
            sharemsg="Check out this resource on Github Learning Lab"
            url={window.location.href}
          />
        </div>
      </div>
      <Rectangle />
      <Subscribe />
    </>
  );
}

export default ResourceDetail;
