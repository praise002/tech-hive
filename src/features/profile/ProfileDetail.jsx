import ArticleCard from '../../components/common/ArticleCard';
import Text from '../../components/common/Text';

const article = {
  image: '/src/assets/articles/the-future-ui-ux.jpg',
  title: 'The Power of Data: How Analytics is Driving Business Decisions',
  description:
    'Learn how data analytics is transforming industries and helping businesses make smarter, data-driven decisions...',
  tags: ['Data Analytics', 'Business', 'Technology'],
  reactions: ['❤️', '😍', '👍', '🔥'],
  reactionsCount: 105,
  posted: '1 week ago',
  readTime: '7 min',
};

function ProfileDetail() {
  return (
    <div className="mt-15">
      <div className="bg-light w-full h-40 relative">
        <div className="absolute transform -translate-x-1/2 top-30 md:top-1/2 left-1/2 flex flex-col items-center">
          <div>
            <div className="relative">
              <img
                className="w-20 h-20 md:w-40 md:h-40"
                src="/src/assets/icons/Avatars.png"
                alt=""
              />
            </div>
          </div>

          <div className="flex flex-col justify-center items-center">
            <Text
              variant="h3"
              size="lg"
              bold={false}
              className="font-semibold mb-1 text-gray-900 dark:text-custom-white"
            >
              Elizabeth Stone
            </Text>
            <p className="text-secondary text-sm">Joined 27th January 2025</p>
          </div>
        </div>
      </div>

      <div className="text-gray-900 dark:text-custom-white mt-30 md:mt-50 flex-col items-center md:items-start md:flex-row flex gap-4 mb-8 px-20">
        <div className="p-3 md:w-fit md:h-fit border border-gray rounded-lg">
          <div className="flex gap-2 items-center mb-2">
            <div className="w-4 h-4">
              <img
                className="w-full h-full dark:invert"
                src="/src/assets/icons/Chat.png"
                alt=""
              />
            </div>
            <div>
              <p className="font-semibold text-xs sm:text-sm md:text-lg">
                0 Comments{' '}
              </p>
            </div>
          </div>
          <div className="flex gap-2 items-center">
            <div className="w-4 h-4">
              <img
                className="w-full h-full dark:invert"
                src="/src/assets/icons/bookmark-light.png"
                alt=""
              />
            </div>
            <p className="font-semibold text-xs sm:text-sm md:text-lg">
              0 Saved{' '}
            </p>
          </div>
        </div>
        <div className="flex-1 flex flex-col gap-4">
          <div className="p-4 border border-gray rounded-lg">
            <Text
              variant="h3"
              size="lg"
              bold={false}
              className="font-semibold mb-2 dark:text-custom-white"
            >
              Recent Comments
            </Text>
            <div>
              <Text
                variant="h3"
                size="base"
                bold={false}
                className="font-semibold mb-2 dark:text-custom-white"
              >
                Africa Fintech Summit 2024
              </Text>
              <p className="text-secondary text-sm mb-1">
                Africa Fintech Summit
              </p>
            </div>
            <div className="flex items-center gap-2 text-xs md:text-sm">
              <p className="font-bold">Thanks for the info</p>
              <p className="text-secondary">27th January, 2025</p>
            </div>
          </div>

          <div className="p-4 border border-gray rounded-lg">
            <Text
              variant="h3"
              size="lg"
              bold={false}
              className="font-semibold mb-1 md:text-2xl dark:text-custom-white"
            >
              Saved Articles
            </Text>
            <ArticleCard article={article} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default ProfileDetail;
