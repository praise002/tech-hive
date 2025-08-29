import { MdLibraryBooks } from 'react-icons/md';
import { BiMessageRounded } from 'react-icons/bi';

import { useState } from 'react';
import CommentsContent from '../componenets/CommentsContent';
import PublishedContent from '../componenets/PublishedContent';
import Text from '../../../components/common/Text';

// import { useProfile } from './useProfile';
// import Spinner from '../../components/common/Spinner';
// import { BsFillArchiveFill } from 'react-icons/bs';

function ProfileDetail() {
  const [isActiveTab, setIsActiveTab] = useState('saved');
  // const { isPending, isError, profile, error } = useProfile();

  // const {
  //   first_name: firstName,
  //   last_name: lastName,
  //   avatar_url: avatarUrl,
  // } = profile;

  // if (isPending)
  //   return (
  //     <div className="min-h-screen flex items-center justify-center">
  //       <Spinner />
  //     </div>
  //   );

  // if (isError) {
  //   // TODO: STYLE LETER
  //   return <span>Error: {error?.message}</span>;
  // }

  const profileTabs = [
    {
      id: 'comments',
      label: 'Comments',
      icon: <BiMessageRounded className="w-5 h-5" />,
      comments: [6, 10, 15],
    },

    {
      id: 'published',
      label: 'Published Articles',
      icon: <MdLibraryBooks className="w-5 h-5" />,
      published: [1005, 1006],
    },
  ];

  function getContent() {
    switch (isActiveTab) {
      case 'comments':
        return <CommentsContent />;
      case 'published':
        return <PublishedContent />;
      default:
        return <CommentsContent />;
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
                // src={avatarUrl || "/assets/icons/Avatars.png"}
                src="/assets/icons/Avatars.png"
                // alt={`${firstName} ${lastName}'s profile picture` || "Elizabeth Stone's profile picture"}
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
              {/* {`${firstName} ${lastName}` || 'Elizabeth Stone'} */}
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
