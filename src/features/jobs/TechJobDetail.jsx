import Text from '../../components/common/Text';

function TechJobDetail() {
  return (
    <div className='border-[#C1C8C7]'>
      <div>
        <Text
          variant="h3"
          size="xl"
          bold={false}
          className="font-semibold text-gray-900 mb-2"
        >
          Frontend Developer
        </Text>
        <div className="text-[#889392] text-sm">TechGiant Inc</div>
      </div>
      {/* Tags Section */}
      <div className="flex gap-2 flex-wrap mb-4">
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
      <div>
        {/* Description */}
        <div>
          <Text
            variant="h5"
            size="lg"
            bold={false}
            className="font-semibold text-gray-900 mb-2"
          >
            Job Description
          </Text>
          <p className="text-[#262A2A]">
            TechGiant Inc is looking for a skilled frontend developer to join
            their dynamic team. You will be responsible for designing and
            implementing user interfaces for our web applications, ensuring an
            exceptional user experience.
          </p>
        </div>

        {/* Requirement */}
        <div>
          <Text
            variant="h5"
            size="lg"
            bold={false}
            className="font-semibold text-gray-900 mb-2"
          >
            Requirements
          </Text>
          <p className="text-[#262A2A]">
            Proficiency in HTML, CSS, and JavaScript. Experience with frameworks
            like React, Angular, or Vue.js. Familiarity with version control
            tools like Git. Strong problem-solving skills and attention to
            detail.
          </p>
        </div>

        {/* Responsibilities */}
        <div>
          <Text
            variant="h5"
            size="lg"
            bold={false}
            className="font-semibold text-gray-900 mb-2"
          >
            Responsibilities
          </Text>
          <p className="text-[#262A2A]">
            Develop and maintain responsive web applications. Collaborate with
            backend developers to integrate APIs. Write clean, scalable code
            using JavaScript frameworks. Optimize applications for maximum speed
            and scalability. Stay up-to-date with emerging technologies and
            trends in frontend development.
          </p>
        </div>

        {/* Job Link */}
        <div>
          <Text
            variant="h5"
            size="lg"
            bold={false}
            className="font-semibold text-gray-900 mb-2"
          >
            How to Apply
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

export default TechJobDetail;
