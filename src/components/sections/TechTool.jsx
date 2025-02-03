import Button from '../common/Button';
import Text from '../common/Text';
import Tool from '../common/Tool';

function TechTool() {
  return (
    <div>
      <div className="my-4">
        <Text
          variant="h3"
          size="xl"
          bold={false}
          className="font-semibold sm:2xl"
        >
          Featured Tech Tool
        </Text>
        <div className="w-[20px]">
          <hr className="border-b-2 border-[#a32816]" />
        </div>
      </div>
      <Tool />
      <Button>Explore More Tools &rarr;</Button>
    </div>
  );
}

export default TechTool;

const tools = [
  {
    toolImage: '',
    toolName: 'Figma',
    toolDescription:
      'A cloud-based design tool for creating, prototyping, and collaborating on user interfaces.',
    toolCategories: ['Design', 'UI/UX', 'Collaboration'],
    callToAction: 'Try Figma for Free',
  },
  {
    toolImage: '',
    toolName: 'Notion',
    toolDescription:
      'An all-in-one workspace for notes, tasks, databases, and collaboration.',
    toolCategories: ['Productivity', 'Organization', 'Teamwork'],
    callToAction: 'Get Started with Notion',
  },
  {
    toolImage: '',
    toolName: 'TensorFlow',
    toolDescription:
      'An open-source platform for building and deploying machine learning models at scale.',
    toolCategories: [
      'Machine Learning',
      'Artificial Intelligence',
      'Data Science',
    ],
    callToAction: 'Explore TensorFlow',
  },
  {
    toolImage: '',
    toolName: 'GitHub',
    toolDescription:
      'A web-based platform for version control, code hosting, and collaboration in software development.',
    toolCategories: ['Development', 'Version Control', 'Collaboration'],
    callToAction: 'Sign Up for GitHub',
  },
  {
    toolImage: '',
    toolName: 'Canva',
    toolDescription:
      'A graphic design platform that allows users to create visual content easily and professionally.',
    toolCategories: ['Design', 'Graphics', 'Marketing'],
    callToAction: 'Start Designing with Canva',
  },
  {
    toolImage: '',
    toolName: 'Slack',
    toolDescription:
      'A communication and collaboration platform designed for teams and businesses.',
    toolCategories: ['Communication', 'Teamwork', 'Productivity'],
    callToAction: 'Try Slack for Free',
  },
  {
    toolImage: '',
    toolName: 'Jira',
    toolDescription:
      'A project management tool used for agile software development, issue tracking, and team collaboration.',
    toolCategories: ['Project Management', 'Agile', 'Software Development'],
    callToAction: 'Start Using Jira',
  },
  {
    toolImage: '',
    toolName: 'Docker',
    toolDescription:
      'A platform for developing, shipping, and running applications using containerization technology.',
    toolCategories: ['DevOps', 'Containerization', 'Automation'],
    callToAction: 'Learn More About Docker',
  },
];
