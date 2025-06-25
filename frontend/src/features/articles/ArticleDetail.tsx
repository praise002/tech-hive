import Bookmark from '../../components/common/Bookmark';
import Image from '../../components/common/Image';
import Rectangle from '../../components/common/Rectangle';
import SocialLinks from '../../components/common/SocialLinks';
import Tags from '../../components/common/Tags';
import Text from '../../components/common/Text';
import CategoryBar from '../../components/sections/CategoryBar';
import Subscribe from '../../components/sections/Subscribe';
import DiscussionThread from '../../components/common/DiscussionThread';
import Reaction from '../../components/common/Reaction';

function ArticleDetail() {
  const article = {
    title: 'The Future of UI/UX: Trends to Watch in 2024',
    image: '/src/assets/articles/the-future-ui-ux.jpg',
    timePosted: '1 hour',
    content: `From AI-powered interfaces to immersive experiences, here are the
                key trends shaping UI/UX design and how designers can stay ahead
                designers must anticipate and adapt to these emerging trends. The
                rise of AI is poised to revolutionize user interactions, with
                chatbots, voice assistants, and personalized recommendations
                becoming increasingly prevalent. Designers will need to focus on
                creating intuitive and human-centered AI interactions, ensuring
                that these technologies enhance rather than hinder the user
                experience. Furthermore, Virtual Reality (VR), Augmented Reality
                (AR), and Mixed Reality (MR) are poised to redefine how we engage
                with digital content. Designers will need to explore new ways to
                create immersive and engaging user experiences in these emerging
                technologies. As data collection and analysis become more
                sophisticated, users will expect hyper-personalized experiences
                tailored to their individual needs and preferences. Designers will
                need to leverage data and AI to create truly personalized
                interfaces while maintaining user privacy and trust. Accessibility
                will continue to be a crucial consideration. Designers must ensure
                that their interfaces are usable by people with disabilities,
                including those with visual, auditory, motor, and cognitive
                impairments. Environmental sustainability will also become an
                increasingly important factor in design decisions. Designers will
                need to prioritize energy efficiency, reduce e-waste, and create
                interfaces that minimize their environmental impact. Lastly, the
                rise of no-code/low-code tools is empowering individuals and
                businesses to create digital experiences without extensive coding
                knowledge. Designers will need to adapt to this changing landscape
                and learn to collaborate effectively with citizen developers. By
                staying informed about these trends and adapting their skills
                accordingly, designers can ensure they remain at the forefront of
                the ever-evolving UI/UX landscape.`,
    url: 'https://dev.to/praise002/hacktoberfest-2024-my-contributor-experience-4mf1',
    author: {
      name: 'Bob Janet',
      image: '/src/assets/icons/profile.jpg',
    },
  };
  const tags = ['UIUXDesign', 'UserExperience', 'InterfaceDesign'];

  return (
    <>
      <CategoryBar />
      <div className="flex flex-col md:flex-row gap-8 px-4 md:px-10 py-8">
        {/* Left Column: Social Links */}
        <div className="hidden md:block px-10 mt-70">
          <SocialLinks
            visible={true}
            title={article.title}
            url={article.url}
            content={article.content}
            sharemsg={article.title}
          />
        </div>

        {/* Right Column: Content */}
        <div className="w-full md:w-3/4 mt-20 md:mt-10 border border-gray rounded-tl-lg rounded-tr-lg overflow-hidden">
          <Image
            alt="Article Image"
            src={article.image}
            className="w-full h-auto shadow-md"
          />
          <div className="px-4 py-6 border border-secondary text-primary">
            <div className="my-4 text-xs text-secondary">
              Posted {article.timePosted} ago
            </div>
            <Text
              variant="h3"
              size="xl"
              bold={false}
              className="font-semibold dark:text-custom-white"
            >
              {article.title}
            </Text>

            {/* Optional Author if a contributor */}
            <div className="flex items-center gap-4 my-4">
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-full overflow-hidden">
                  <Image
                    alt="Author"
                    src={article.author.image}
                    className="w-full h-full"
                  />
                </div>
                <Text
                  variant="h3"
                  size="base"
                  bold={false}
                  className="dark:text-custom-white"
                >
                  {article.author.name}
                </Text>
              </div>
            </div>

            <p className="text-base md:text-lg leading-relaxed dark:text-custom-white">
              {article.content}
            </p>
            <Tags tags={tags} />
            <div className="flex justify-between my-4">
              <Reaction />
              <div>
                <Bookmark className="w-6 h-6 dark:invert" />
              </div>
            </div>
            <DiscussionThread />
          </div>
        </div>

        {/* Mobile social link */}
        <div className="block md:hidden">
          <SocialLinks
            visible={true}
            title={article.title}
            url={article.url}
            content={article.content}
            sharemsg={article.title}
          />
        </div>
      </div>
      <Rectangle />
      <Subscribe />
    </>
  );
}

export default ArticleDetail;
