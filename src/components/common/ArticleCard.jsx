import Description from './Description';
import Image from './Image';
import ArticleReactions from './ArticleReactions';
import Tags from './Tags';
import ArticleTitle from './ArticleTitle';
import Button from './Button';

function ArticleCard() {
  return (
    <>
      <div className="relative overflow-hidden rounded-lg shadow-lg">
        <Image alt="Article" src="/src/assets/articles/the-future-ui-ux.png" />
        <div className="p-5 border-l border-r border-b border-[#C1C8C7] rounded-bl-lg rounded-br-lg overflow-hidden">
          <ArticleTitle />
          <Description>
            From AI-powered interfaces to immersive experiences, here are the
            key trends shaping UI/UX design and how designers can stay ahead...
          </Description>
          <Tags />
          <Button variant="outline">View details</Button>
          <ArticleReactions />
        </div>
      </div>
      {/* <div className="relative overflow-hidden rounded-lg shadow-lg flex">
        <Image alt="Article" src="/src/assets/articles/the-future-ui-ux.png" />
        <div className="p-5 border-t border-r border-b border-[#C1C8C7] rounded-br-lg rounded-tr-lg overflow-hidden">
          <ArticleTitle />
          <ArticleDescription />
          <Tags />
          <Button variant="outline">View details</Button>
          <ArticleReactions />
        </div>
      </div> */}
    </>
  );
}

export default ArticleCard;

const articles = [
  {
    image: '', // Add image URL here
    title: 'The Future of UI/UX: Trends to Watch in 2024',
    description:
      'From AI-powered interfaces to immersive experiences, here are the key trends shaping UI/UX design and how designers can stay ahead...',
    tags: ['UI/UX Design', 'User Experience', 'Interface Design'],
    reactions: ['❤️', '😍', '👍', '🔥'],
    reactionsCount: 100,
    posted: '1 day ago',
    readTime: '3 min',
  },
  {
    image: '', // Add image URL here
    title: 'Top 5 Programming Languages to Learn in 2024',
    description:
      "Discover which coding languages are leading the tech revolution this year, and why they're essential for your career growth...",
    tags: ['Programming', 'Web Development', 'Open Source'],
    reactions: ['❤️', '😍', '👍', '🔥'],
    reactionsCount: 85,
    posted: '1 day ago',
    readTime: '5 min',
  },
  {
    image: '', // Add image URL here
    title: 'How AI is Transforming Healthcare in 2024',
    description:
      'Explore the groundbreaking ways artificial intelligence is revolutionizing healthcare, from diagnostics to personalized medicine...',
    tags: ['AI', 'Healthcare', 'Innovation'],
    reactions: ['❤️', '😍', '👍', '🔥'],
    reactionsCount: 120,
    posted: '2 days ago',
    readTime: '7 min',
  },
  {
    image: '', // Add image URL here
    title: 'The Rise of Remote Work: Tools and Tips for Success',
    description:
      'Remote work is here to stay. Learn about the best tools and strategies to thrive in a distributed work environment...',
    tags: ['Remote Work', 'Productivity', 'Collaboration'],
    reactions: ['❤️', '😍', '👍', '🔥'],
    reactionsCount: 95,
    posted: '3 days ago',
    readTime: '6 min',
  },
  {
    image: '', // Add image URL here
    title: 'Blockchain Beyond Cryptocurrency: Real-World Applications',
    description:
      'Discover how blockchain technology is being used in industries like supply chain, healthcare, and finance...',
    tags: ['Blockchain', 'Technology', 'Innovation'],
    reactions: ['❤️', '😍', '👍', '🔥'],
    reactionsCount: 75,
    posted: '4 days ago',
    readTime: '8 min',
  },
  {
    image: '', // Add image URL here
    title: 'The Ethics of AI: Balancing Innovation and Responsibility',
    description:
      'As AI becomes more powerful, ethical considerations are more important than ever. Learn about the challenges and solutions...',
    tags: ['AI Ethics', 'Technology', 'Responsibility'],
    reactions: ['❤️', '😍', '👍', '🔥'],
    reactionsCount: 110,
    posted: '5 days ago',
    readTime: '9 min',
  },
  {
    image: '', // Add image URL here
    title: 'Cybersecurity in 2024: Threats and Best Practices',
    description:
      'Stay ahead of cyber threats with the latest trends and best practices in cybersecurity for individuals and businesses...',
    tags: ['Cybersecurity', 'Technology', 'Best Practices'],
    reactions: ['❤️', '😍', '👍', '🔥'],
    reactionsCount: 90,
    posted: '6 days ago',
    readTime: '10 min',
  },
  {
    image: '', // Add image URL here
    title: 'The Future of E-Commerce: Trends to Watch',
    description:
      'From AI-driven personalization to sustainable practices, explore the trends shaping the future of online shopping...',
    tags: ['E-Commerce', 'Technology', 'Trends'],
    reactions: ['❤️', '😍', '👍', '🔥'],
    reactionsCount: 80,
    posted: '1 week ago',
    readTime: '6 min',
  },
  {
    image: '', // Add image URL here
    title: 'The Power of Data: How Analytics is Driving Business Decisions',
    description:
      'Learn how data analytics is transforming industries and helping businesses make smarter, data-driven decisions...',
    tags: ['Data Analytics', 'Business', 'Technology'],
    reactions: ['❤️', '😍', '👍', '🔥'],
    reactionsCount: 105,
    posted: '1 week ago',
    readTime: '7 min',
  },
  {
    image: '', // Add image URL here
    title: "The Evolution of Cloud Computing: What's Next?",
    description:
      'From hybrid clouds to serverless architectures, explore the future of cloud computing and its impact on businesses...',
    tags: ['Cloud Computing', 'Technology', 'Innovation'],
    reactions: ['❤️', '😍', '👍', '🔥'],
    reactionsCount: 70,
    posted: '2 weeks ago',
    readTime: '8 min',
  },
];
