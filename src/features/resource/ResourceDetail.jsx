import Image from '../../components/common/Image';
import Text from '../../components/common/Text';

function ResourceDetail() {
  return (
    <div className="border-[#C1C8C7]">
      <Image alt="Figma" src="/src/assets/resources/github-learning-lab.png" />
      <div>
        <Text
          variant="h3"
          size="lg"
          bold={false}
          className="font-semibold text-gray-900 mb-2"
        >
          Github Learning Lab
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
            GitHub Learning Lab is an educational platform offering interactive,
            project-based courses to improve your skills in software
            development, version control, and open-source collaboration.
          </p>
        </div>

        {/* Popular Courses */}
        <ul>
          <Text
            variant="h5"
            size="lg"
            bold={false}
            className="font-semibold text-gray-900 mb-2"
          >
            Popular Courses
          </Text>
          <li>Introduction to Git and GitHub.</li>
          <li>Building RESTful APIs.</li>
          <li>Works on any platform with an internet connection.</li>
          <li>Advanced topics in software development.</li>
        </ul>

        {/* Why Learn Here? */}
        <ul>
          <Text
            variant="h5"
            size="lg"
            bold={false}
            className="font-semibold text-gray-900 mb-2"
          >
            Why Learn Here?
          </Text>
          <li>Hands-on exercises with real-world applications.</li>
          <li>Earn certificates of completion to showcase your skills.</li>
          <li>Supportive community of learners and mentors.</li>
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
              href="https://www.github.com"
              target="_blank"
              rel="noopener noreferrer"
            >
              https://www.github.com
            </a>
          </div>
        </div>
      </div>
      <div className="text-[#889392] text-sm">Posted 1 hour ago</div>
    </div>
  );
}

export default ResourceDetail;
