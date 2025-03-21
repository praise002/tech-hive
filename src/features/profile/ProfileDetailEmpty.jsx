import { RiDraftFill } from 'react-icons/ri';
import { MdArticle, MdLibraryBooks } from 'react-icons/md';
import { BiMessageRounded } from 'react-icons/bi';

import Bookmark from '../../components/common/Bookmark';
import Text from '../../components/common/Text';
import { useState } from 'react';

function ProfileDetailEmpty() {
  const [isActiveTab, setIsActiveTab] = useState('saved');

  const profileTabs = [
    {
      id: 'saved',
      label: 'Saved',
      icon: <Bookmark className="w-5 h-5" />,
    },
    {
      id: 'comments',
      label: 'Comments',
      icon: <BiMessageRounded className="w-5 h-5" />,
    },
    {
      id: 'drafts',
      label: 'Drafts',
      icon: <RiDraftFill className="w-5 h-5" />,
    },
    {
      id: 'submitted',
      label: 'Submitted Articles',
      icon: <MdArticle className="w-5 h-5" />,
    },
    {
      id: 'published',
      label: 'Published Articles',
      icon: <MdLibraryBooks className="w-5 h-5" />,
    },
  ];

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
            <div className="absolute top-1/3 right-10 md:right-1 md:top-1/2 bg-light rounded-full p-1 md:p-2">
              <img
                className="w-5 h-5 md:w-7 md:h-7"
                src="/src/assets/icons/mynaui_edit.png"
                alt=""
              />
            </div>
          </div>

          <div className="flex flex-col justify-center items-center">
            <Text
              variant="h3"
              size="lg"
              bold={false}
              className="font-semibold text-gray-900 dark:text-custom-white mb-1"
            >
              Elizabeth Stone
            </Text>
            <p className="text-secondary text-sm">Joined 27th January 2025</p>
          </div>
        </div>
      </div>

      <div className="flex flex-col gap-4 items-center mt-30 md:mt-50">
        <div className="flex bg-light gap-2 p-2 rounded-md">
          {profileTabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setIsActiveTab(tab.id)}
              className={`flex p-2 items-center gap-1 rounded-md cursor-pointer ${
                isActiveTab === tab.id && 'bg-red text-custom-white'
              }`}
            >
              <span>{tab.icon}</span>
              <span>{tab.label}</span>
            </button>
          ))}
        </div>

        <div className="flex-1 py-8 flex justify-center items-center ">
          <div className="md:w-xs w-60 dark:text-custom-white">
            <img
              className="w-full h-full"
              src="/src/assets/icons/amico.png"
              alt="An empty profile"
            />
            <div className="text-xs md:text-sm text-center mt-4">
              No saved articles yet!
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ProfileDetailEmpty;
