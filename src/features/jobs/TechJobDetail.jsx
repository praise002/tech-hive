import Rectangle from '../../components/common/Rectangle';
import SocialLinks from '../../components/common/SocialLinks';
import Text from '../../components/common/Text';
import CategoryBar from '../../components/sections/CategoryBar';
import Subscribe from '../../components/sections/Subscribe';

function TechJobDetail() {
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
              Frontend Developer
            </Text>
            <div className="text-[#889392] text-sm">TechGiant Inc</div>
          </div>

          {/* Tags Section */}
          <div className="flex gap-2 flex-wrap my-4">
            <span className="inline-flex items-center px-2 py-1 bg-[#FFEDDD] text-xs font-medium text-gray-700 rounded-sm">
              🌍 Remote
            </span>
            <span className="inline-flex items-center px-2 py-1 bg-[#FFEDDD] text-xs font-medium text-gray-700 rounded-sm">
              ⚛️ React
            </span>
            <span className="inline-flex items-center px-2 py-1 bg-[#FFEDDD] text-xs font-medium text-gray-700 rounded-sm">
              🟨 JavaScript
            </span>
            <span className="inline-flex items-center px-2 py-1 bg-[#FFEDDD] text-xs font-medium text-gray-700 rounded-sm">
              ⏳ Full-time
            </span>
          </div>

          <div className="space-y-8 text-[#262A2A]">
            {/* Description */}
            <div>
              <Text
                variant="h5"
                size="lg"
                bold={false}
                className="font-semibold mb-2"
              >
                Job Description
              </Text>
              <p className="text-base md:text-lg leading-relaxed">
                TechGiant Inc is looking for a skilled frontend developer to
                join their dynamic team. You will be responsible for designing
                and implementing user interfaces for our web applications,
                ensuring an exceptional user experience.
              </p>
            </div>

            {/* Requirement */}
            <div>
              <Text
                variant="h5"
                size="lg"
                bold={false}
                className="font-semibold mb-2"
              >
                Requirements
              </Text>
              <ul className="list-disc pl-6 space-y-2 text-base md:text-lg leading-relaxed">
                <li>Proficiency in HTML, CSS, and JavaScript.</li>
                <li>
                  Experience with frameworks like React, Angular, or Vue.js.
                </li>
                <li>Familiarity with version control tools like Git.</li>
                <li>Strong problem-solving skills and attention to detail.</li>
              </ul>
            </div>

            {/* Responsibilities */}
            <div>
              <Text
                variant="h5"
                size="lg"
                bold={false}
                className="font-semibold mb-2"
              >
                Responsibilities
              </Text>
              <p className="text-base md:text-lg leading-relaxed">
                Develop and maintain responsive web applications. Collaborate
                with backend developers to integrate APIs. Write clean, scalable
                code using JavaScript frameworks. Optimize applications for
                maximum speed and scalability. Stay up-to-date with emerging
                technologies and trends in frontend development.
              </p>
            </div>

            {/* Job Link */}
            <div>
              <Text
                variant="h5"
                size="lg"
                bold={false}
                className="font-semibold mb-2"
              >
                How to Apply
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
          <div className="text-[#889392] text-sm my-4">Posted 1 hour ago</div>
        </div>

        {/* Mobile social link */}
        <div className="block md:hidden px-10">
          <SocialLinks visible={false} />
        </div>
      </div>

      <Rectangle />
      <Subscribe />
    </>
  );
}

export default TechJobDetail;
