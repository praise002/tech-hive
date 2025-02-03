import Button from './Button';
import Description from './Description';
import Image from './Image';
import Tags from './Tags';
import Text from './Text';

function Resource() {
  return (
    <div className="relative overflow-hidden rounded-lg shadow-lg">
      <Image
        alt="GitHub Learning Lab"
        src="/src/assets/resources/github-learning-lab.png"
      />

      <div className="p-5 border-l border-r border-b border-[#C1C8C7] rounded-bl-lg rounded-br-lg overflow-hidden">
        <Text variant="h4" size="xl" bold={false} className="font-semibold">
          GitHub Learning Lab
        </Text>
        <div className="text-xs text-[#889392]">Educational Platform</div>

        <Description>
          Interactive coding courses and project-based learning to improve your
          skills in software development and version control.
        </Description>

        <Tags />
        <Button variant="outline">View details</Button>
        <div className="mt-2 text-xs text-[#889392]">Posted 1 day ago</div>
      </div>
    </div>
  );
}

export default Resource;

const resources = [
  {
    resourceImage: '',
    resourceName: 'GitHub Learning Lab',
    resourceType: 'Educational Platform',
    resourceDescription:
      'Interactive coding courses and project-based learning to improve your skills in software development and version control.',
    resourceCategories: [
      'SoftwareDevelopment',
      'VersionControl',
      'OpenSource',
      'BeginnerFriendly',
    ],
    timePosted: '1 day ago',
  },
  {
    resourceImage: '',
    resourceName: 'FreeCodeCamp',
    resourceType: 'Coding Community',
    resourceDescription:
      'A comprehensive programming curriculum with hands-on projects and certifications in web development, algorithms, and data structures.',
    resourceCategories: [
      'WebDevelopment',
      'DataStructures',
      'Algorithms',
      'BeginnerFriendly',
    ],
    timePosted: '1 day ago',
  },
  {
    resourceImage: '',
    resourceName: 'Coursera',
    resourceType: 'Online Learning Platform',
    resourceDescription:
      'University-backed courses and specializations in technology, computer science, machine learning, cloud computing, and UX design.',
    resourceCategories: [
      'MachineLearning',
      'CloudComputing',
      'UXDesign',
      'Python',
      'BeginnerFriendly',
    ],
    timePosted: '1 day ago',
  },
  {
    resourceImage: '',
    resourceName: 'Khan Academy',
    resourceType: 'Educational Website',
    resourceDescription:
      'Free courses on a wide range of subjects, including math, science, programming, and more, suitable for all levels of learners.',
    resourceCategories: [
      'Mathematics',
      'Science',
      'Programming',
      'BeginnerFriendly',
    ],
    timePosted: '2 days ago',
  },
  {
    resourceImage: '',
    resourceName: 'Udemy',
    resourceType: 'E-Learning Marketplace',
    resourceDescription:
      'A vast library of courses taught by experts, covering topics like coding, business, design, and personal development.',
    resourceCategories: [
      'WebDevelopment',
      'BusinessSkills',
      'Design',
      'PersonalGrowth',
    ],
    timePosted: '3 days ago',
  },
  {
    resourceImage: '',
    resourceName: 'edX',
    resourceType: 'Online Education Platform',
    resourceDescription:
      'High-quality courses from top universities and institutions in fields such as computer science, engineering, and data analysis.',
    resourceCategories: [
      'ComputerScience',
      'Engineering',
      'DataAnalysis',
      'AdvancedLearning',
    ],
    timePosted: '4 days ago',
  },
  {
    resourceImage: '',
    resourceName: 'LeetCode',
    resourceType: 'Algorithm Practice Platform',
    resourceDescription:
      'A platform for practicing coding challenges and preparing for technical interviews with a focus on algorithms and data structures.',
    resourceCategories: [
      'Algorithms',
      'DataStructures',
      'InterviewPrep',
      'IntermediateLevel',
    ],
    timePosted: '5 days ago',
  },
  {
    resourceImage: '',
    resourceName: 'MDN Web Docs',
    resourceType: 'Web Development Documentation',
    resourceDescription:
      'Comprehensive guides and references for web technologies, including HTML, CSS, JavaScript, and APIs.',
    resourceCategories: [
      'WebDevelopment',
      'Frontend',
      'Backend',
      'ReferenceMaterial',
    ],
    timePosted: '6 days ago',
  },
  {
    resourceImage: '',
    resourceName: 'Stack Overflow',
    resourceType: 'Q&A Community',
    resourceDescription:
      'A community-driven platform where developers ask and answer questions related to programming and software development.',
    resourceCategories: [
      'Programming',
      'ProblemSolving',
      'CommunitySupport',
      'AllLevels',
    ],
    timePosted: '7 days ago',
  },
  {
    resourceImage: '',
    resourceName: 'The Odin Project',
    resourceType: 'Open-Source Curriculum',
    resourceDescription:
      'A free and open-source full-stack web development curriculum with interactive projects and exercises.',
    resourceCategories: [
      'WebDevelopment',
      'FullStack',
      'OpenSource',
      'BeginnerFriendly',
    ],
    timePosted: '8 days ago',
  },
];
