import { RiDraftFill } from 'react-icons/ri';
import { MdArticle, MdLibraryBooks } from 'react-icons/md';
import { BiMessageRounded } from 'react-icons/bi';
import { FaRegBookmark } from 'react-icons/fa6';
// import ArticleCard from '../../components/common/ArticleCard';
import Text from '../../components/common/Text';
import { useState } from 'react';
import Articles from '../../components/sections/Articles';
import { BsFillArchiveFill } from 'react-icons/bs';

// const article = {
//   image: '/assets/articles/the-future-ui-ux.jpg',
//   title: 'The Power of Data: How Analytics is Driving Business Decisions',
//   description:
//     'Learn how data analytics is transforming industries and helping businesses make smarter, data-driven decisions...',
//   tags: ['Data Analytics', 'Business', 'Technology'],
//   reactions: ['❤️', '😍', '👍', '🔥'],
//   reactionsCount: 105,
//   posted: '1 week ago',
//   readTime: '7 min',
// };

function ProfileDetail() {
  const [isActiveTab, setIsActiveTab] = useState('saved');

  const profileTabs = [
    {
      id: 'saved',
      label: 'Saved',
      icon: <FaRegBookmark className="w-5 h-5" />,
      articles: [1001, 1002, 1004], // find the article in articles use find() or filter()
    },
    {
      id: 'comments',
      label: 'Comments',
      icon: <BiMessageRounded className="w-5 h-5" />,
      comments: [6, 10, 15],
    },
    {
      id: 'drafts',
      label: 'Drafts',
      icon: <RiDraftFill className="w-5 h-5" />,
      drafts: [4, 6, 8],
    },
    {
      id: 'submitted',
      label: 'Submitted Articles',
      icon: <MdArticle className="w-5 h-5" />,
      submitted: [10, 16, 2],
    },
    {
      id: 'published',
      label: 'Published Articles',
      icon: <MdLibraryBooks className="w-5 h-5" />,
      published: [1005, 1006],
    },
    {
      id: 'archived',
      label: 'Archived Articles',
      icon: <BsFillArchiveFill className="w-5 h-5" />,
      published: [1005, 1006],
    },
  ];

  function SavedContent() {
    return (
      <>
        {/* <div className="md:w-xs w-60 dark:text-custom-white">
          <img
            className="w-full h-full"
            src="/assets/icons/amico.png"
            alt="An empty profile"
          />
          <div className="text-xs md:text-sm text-center mt-4">
            No saved articles yet!
          </div>
        </div> */}
        <Text
          variant="h3"
          size="lg"
          bold={false}
          className="font-semibold mb-1 md:text-2xl dark:text-custom-white lg:mt-4 px-4 lg:px-8"
        >
          Saved Articles
        </Text>
        {/* <div className="grid grid-cols-1 gap-4 lg:grid-cols-2 xl:grid-cols-3">
          <ArticleCard article={article} />
          <ArticleCard article={article} />
          <ArticleCard article={article} />
          <ArticleCard article={article} />
        </div> */}
        <Articles marginTop={8} visibleHeader={false} />
      </>
    );
  }

  function CommentsContent() {
    return (
      // <p className="font-bold text-sm">No recent comments available.</p>
      <>
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
          <p className="text-secondary text-sm mb-1">Africa Fintech Summit</p>
        </div>
        <div className="flex items-center gap-2 text-xs md:text-sm">
          <p className="font-bold">Thanks for the info</p>
          <p className="text-secondary">27th January, 2025</p>
        </div>
      </>
    );
  }

  function DraftsContent() {
    return (
      <>
        {/* <div className="md:w-xs w-60 dark:text-custom-white">
          <img
            className="w-full h-full"
            src="/assets/icons/amico.png"
            alt="An empty profile"
          />
          <div className="text-xs md:text-sm text-center mt-4">
            No drafts available.
          </div>
        </div> */}
        <Text
          variant="h3"
          size="lg"
          bold={false}
          className="font-semibold mb-4 dark:text-custom-white"
        >
          My Drafts
        </Text>

        <div className="space-y-4">
          <div className="border border-gray-200 rounded-lg p-4 hover:border-red transition-colors">
            <div className="flex justify-between items-start mb-2">
              <Text
                variant="h3"
                size="base"
                bold={false}
                className="font-semibold dark:text-custom-white"
              >
                Getting Started with React Hooks
              </Text>
              <span className="text-nowrap text-xs px-2 py-1 bg-light rounded-full text-secondary">
                In Progress
              </span>
            </div>

            <p className="text-secondary text-sm mb-3 line-clamp-2">
              React Hooks are a powerful feature that allows you to use state
              and other React features without writing a class component...
            </p>

            <div className="flex items-center gap-4">
              <div className="flex-1 h-2 bg-gray-200 rounded-full">
                <div
                  className="h-full bg-red rounded-full"
                  style={{ width: '75%' }}
                />
              </div>
              <span className="text-xs text-secondary">75% complete</span>
            </div>

            <div className="flex items-center justify-between mt-3 text-xs text-secondary">
              <span>Last edited: May 10, 2025</span>
              <button className="text-red hover:text-red-600 font-medium">
                Continue Editing
              </button>
            </div>
          </div>

          <div className="border border-gray-200 rounded-lg p-4 hover:border-red transition-colors">
            <div className="flex justify-between items-start mb-2">
              <Text
                variant="h3"
                size="base"
                bold={false}
                className="font-semibold dark:text-custom-white"
              >
                Understanding TypeScript Generics
              </Text>
              <span className="text-nowrap text-xs px-2 py-1 bg-light rounded-full text-secondary">
                Just Started
              </span>
            </div>

            <p className="text-secondary text-sm mb-3 line-clamp-2">
              TypeScript generics provide a way to make components work with any
              data type while maintaining type safety...
            </p>

            <div className="flex items-center gap-4">
              <div className="flex-1 h-2 bg-gray-200 rounded-full">
                <div
                  className="h-full bg-red rounded-full"
                  style={{ width: '30%' }}
                />
              </div>
              <span className="text-xs text-secondary">30% complete</span>
            </div>

            <div className="flex items-center justify-between mt-3 text-xs text-secondary">
              <span>Last edited: May 8, 2025</span>
              <button className="text-red hover:text-red-600 font-medium">
                Continue Editing
              </button>
            </div>
          </div>
        </div>
      </>
    );
  }

  function SubmittedContent() {
    return (
      <>
        {/* <p className="font-bold text-sm">No articles submitted.</p> */}
        <Text
          variant="h3"
          size="lg"
          bold={false}
          className="font-semibold mb-4 dark:text-custom-white"
        >
          Submitted Articles
        </Text>

        <div className="space-y-4">
          <div className="border border-gray-200 rounded-lg p-4 hover:border-red transition-colors">
            <div className="flex justify-between mb-2">
              <Text
                variant="h3"
                size="base"
                bold={false}
                className="font-semibold dark:text-custom-white"
              >
                Building Scalable APIs with Node.js
              </Text>
              <span className="text-nowrap flex items-center text-xs px-2 py-1 bg-light rounded-full text-secondary">
                Under Review
              </span>
            </div>

            <p className="text-secondary text-sm mb-3 line-clamp-2">
              Learn best practices for building robust and scalable REST APIs
              using Node.js, Express, and MongoDB...
            </p>

            <div className="flex  justify-between mt-3 text-xs text-secondary">
              <span>Submitted: May 11, 2025</span>
              <div className="flex gap-3">
                <span>Expected review: 2-3 days</span>
                <button className="text-red hover:text-red-600 font-medium">
                  View Details
                </button>
              </div>
            </div>
          </div>

          <div className="border border-gray-200 rounded-lg p-4 hover:border-red transition-colors">
            <div className="flex justify-between mb-2">
              <Text
                variant="h3"
                size="base"
                bold={false}
                className="font-semibold dark:text-custom-white"
              >
                Introduction to Web Accessibility
              </Text>
              <span className="text-nowrap flex items-center text-xs px-2 py-1 bg-light rounded-full text-secondary">
                Pending Review
              </span>
            </div>

            <p className="text-secondary text-sm mb-3 line-clamp-2">
              Discover how to make your websites accessible to everyone by
              implementing WCAG guidelines and best practices...
            </p>

            <div className="flex justify-between mt-3 text-xs text-secondary">
              <span>Submitted: May 9, 2025</span>
              <div className="flex gap-3">
                <span>In review queue</span>
                <button className="text-red hover:text-red-600 font-medium">
                  View Details
                </button>
              </div>
            </div>
          </div>
        </div>
      </>
    );
  }

  function PublishedContent() {
    return (
      <>
        {/* <div className="md:w-xs w-60 dark:text-custom-white">
          <img
            className="w-full h-full"
            src="/assets/icons/amico.png"
            alt="An empty profile"
          />
          <div className="text-xs md:text-sm text-center mt-4">
            No published articles!
          </div>
        </div> */}
        <Text
          variant="h3"
          size="lg"
          bold={false}
          className="font-semibold mb-1 md:text-2xl dark:text-custom-white lg:mt-4 px-4 lg:px-8"
        >
          Published Articles
        </Text>
        {/* <div className="grid grid-cols-1 gap-4 lg:grid-cols-2 xl:grid-cols-3">
          <ArticleCard article={article} />
          <ArticleCard article={article} />
          <ArticleCard article={article} />
          <ArticleCard article={article} />
        </div> */}
        <Articles marginTop={8} showAdminActions={true} visibleHeader={false} />
      </>
    );
  }

  function ArchivedContent() {
    return (
      <>
        {/* <div className="md:w-xs w-60 dark:text-custom-white">
          <img
            className="w-full h-full"
            src="/assets/icons/amico.png"
            alt="An empty profile"
          />
          <div className="text-xs md:text-sm text-center mt-4">
            No archived articles yet!
          </div>
        </div> */}
        <Text
          variant="h3"
          size="lg"
          bold={false}
          className="font-semibold mb-1 md:text-2xl dark:text-custom-white lg:mt-4 px-4 lg:px-8"
        >
          Archived Articles
        </Text>
        <Articles
          marginTop={8}
          visibleHeader={false}
          showAdminActions={true}
          context="archived"
        />
      </>
    );
  }

  function getContent() {
    switch (isActiveTab) {
      case 'saved':
        return <SavedContent />;
      case 'comments':
        return <CommentsContent />;
      case 'drafts':
        return <DraftsContent />;
      case 'submitted':
        return <SubmittedContent />;
      case 'published':
        return <PublishedContent />;
      case 'archived':
        return <ArchivedContent />;
      default:
        return null;
    }
  }

  return (
    <div className="mt-15" aria-label="User profile details">
      <div className="bg-light w-full h-40 relative">
        {/* ✅ SVG Background */}
        <img
          src="/assets/hero-section.svg"
          alt="Background"
          className="pointer-events-none absolute inset-0 w-full h-full object-cover opacity-70"
        />
        <div className="absolute transform -translate-x-1/2 top-30 md:top-1/2 left-1/2 flex flex-col items-center">
          <div>
            <div className="relative">
              <img
                className="w-20 h-20 md:w-40 md:h-40"
                src="/assets/icons/Avatars.png"
                alt="Elizabeth Stone's profile picture"
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

      <div className="max-w-7xl mx-auto sm:px-6 lg:px-8">
        <nav
          className="flex flex-col gap-4 mt-30 md:mt-50"
          aria-label="Profile tabs"
        >
          <div className="flex place-self-center bg-light gap-2 p-2 rounded-md">
            {profileTabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setIsActiveTab(tab.id)}
                className={`flex p-2 items-center gap-2 rounded-md text-xs sm:text-base cursor-pointer ${
                  isActiveTab === tab.id && 'bg-red text-custom-white'
                }`}
                aria-label={`View ${tab.label}`}
                aria-pressed={isActiveTab === tab.id}
              >
                <span className="flex-shrink-0">{tab.icon}</span>
                <span
                  className={`${
                    isActiveTab == tab.id ? 'inline' : 'hidden md:inline'
                  }`}
                >
                  {tab.label}
                </span>
              </button>
            ))}
          </div>

          <div className="py-8">
            {/* flex justify-center */}

            <div className="dark:text-custom-white p-4 md:border border-gray rounded-lg">
              {getContent()}
            </div>
          </div>
        </nav>
      </div>
    </div>
  );
}

export default ProfileDetail;

// NOTE: OTHERS CAN ONLY SEE YOUR COMMENTS AND SUBMITTED ARTICLES IN PROFILEDETAIL VIEW
