import Button from './Button';
import Text from './Text';

function JobPosting() {
  return (
    <div className="p-6 rounded-lg border border-[#C1C8C7] shadow-lg max-w-md mx-auto">
      {/* Job Title */}
      <Text
        variant="h4"
        size="xl"
        bold={false}
        className="font-semibold text-gray-900 mb-2"
      >
        Frontend Developer
      </Text>

      {/* Company Name */}
      <div className="text-[#889392] text-sm">TechGiant Inc</div>

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

      {/* View Details Button */}
      <Button variant="outline" className="font-medium mb-4">
        View Details
      </Button>

      {/* Posted Time */}

      <div className="text-[#889392] text-sm">1 hour ago</div>
    </div>
  );
}

export default JobPosting;

const techJobs = [
  {
    title: 'Frontend Developer',
    company: 'TechGiant Inc',
    tags: ['🌍 Remote', '⚛️ React', '🟨 Javascript', '🕒 Full-time'],
    lastPosted: '1 hour',
  },
  {
    title: 'Data Analyst',
    company: 'Insight Analytics Co.',
    tags: ['🏢 Hybrid', '🐍 Python', '🤖 Machine Learning', '⏰ Part-time'],
    lastPosted: '3 hours',
  },
  {
    title: 'Mobile App Developer',
    company: 'AppNest Studios',
    tags: ['🌍 Remote', '📱 Flutter', '🟪 Kotlin', '🕒 Full-time'],
    lastPosted: '1 day',
  },
  {
    title: 'Backend Developer',
    company: 'Cloudify Solutions',
    tags: ['🌍 Remote', '☕ Java', '🔗 Spring Boot', '🕒 Full-time'],
    lastPosted: '2 days',
  },
  {
    title: 'DevOps Engineer',
    company: 'InfraTech',
    tags: ['🏢 Hybrid', '🐧 Linux', '🐳 Docker', '⚙️ CI/CD'],
    lastPosted: '4 hours',
  },
  {
    title: 'UI/UX Designer',
    company: 'PixelCraft Design',
    tags: ['🌍 Remote', '🎨 Figma', '✏️ Adobe XD', '🕒 Full-time'],
    lastPosted: '6 hours',
  },
  {
    title: 'Cloud Architect',
    company: 'SkyHigh Cloud',
    tags: ['🌍 Remote', '☁️ AWS', '☁️ Azure', '🕒 Full-time'],
    lastPosted: '1 day',
  },
  {
    title: 'AI Engineer',
    company: 'NeuralMind AI',
    tags: ['🏢 Hybrid', '🧠 TensorFlow', '🤖 NLP', '🕒 Full-time'],
    lastPosted: '2 days',
  },
  {
    title: 'Cybersecurity Specialist',
    company: 'SecureNet',
    tags: [
      '🌍 Remote',
      '🔒 Penetration Testing',
      '🛡️ Firewall',
      '🕒 Full-time',
    ],
    lastPosted: '5 hours',
  },
  {
    title: 'Game Developer',
    company: 'PixelPlay Studios',
    tags: ['🏢 Hybrid', '🎮 Unity', '🟦 C#', '🕒 Full-time'],
    lastPosted: '1 day',
  },
  {
    title: 'Blockchain Developer',
    company: 'ChainForge',
    tags: ['🌍 Remote', '⛓️ Solidity', '🔗 Ethereum', '🕒 Full-time'],
    lastPosted: '3 days',
  },
  {
    title: 'Full Stack Developer',
    company: 'CodeCrafters',
    tags: ['🌍 Remote', '⚛️ React', '🟩 Node.js', '🕒 Full-time'],
    lastPosted: '1 hour',
  },
  {
    title: 'QA Engineer',
    company: 'Testify Labs',
    tags: ['🏢 Hybrid', '🧪 Selenium', '🐞 Bug Tracking', '🕒 Full-time'],
    lastPosted: '2 hours',
  },
  {
    title: 'Product Manager',
    company: 'InnovateX',
    tags: ['🏢 Hybrid', '📊 Agile', '📈 Scrum', '🕒 Full-time'],
    lastPosted: '1 day',
  },
  {
    title: 'Technical Writer',
    company: 'DocuCraft',
    tags: ['🌍 Remote', '📝 Documentation', '✍️ Markdown', '⏰ Part-time'],
    lastPosted: '4 days',
  },
];
