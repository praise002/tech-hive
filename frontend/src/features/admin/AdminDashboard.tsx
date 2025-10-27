import { MdKeyboardArrowLeft, MdKeyboardArrowRight } from 'react-icons/md';

import Text from '../../components/common/Text';
import { MdArticle, MdLibraryBooks, MdAnalytics } from 'react-icons/md';

import { useState } from 'react';
import ManagePosts from './ManagePosts';
import ManageContent from './ManageContent';
import Analytics from './Analytics';
import Button from '../../components/common/Button';

function AdminDashboard() {
  const [isActiveTab, setIsActiveTab] = useState('manage posts');

  const adminTabs = [
    {
      id: 'manage posts',
      label: 'Manage posts',
      icon: <MdArticle className="w-5 h-5" />,
    },
    {
      id: 'manage content',
      label: 'Manage content',
      icon: <MdLibraryBooks className="w-5 h-5" />,
    },
    {
      id: 'analytics',
      label: 'Analytics',
      icon: <MdAnalytics className="w-5 h-5" />,
    },
  ];

  function getContent() {
    switch (isActiveTab) {
      case 'manage posts':
        return <ManagePosts />;
      case 'manage content':
        return <ManageContent />;
      case 'analytics':
        return <Analytics />;

      default:
        return null;
    }
  }

  return (
    <div className="dark:text-custom-white">
      <div className="relative mt-12 bg-gradient-to-r from-coral/50 to-peach py-10 px-7 sm:py-20 sm:px-14 h-40">
        {/* ✅ SVG Background */}
        <img
          src="/assets/hero-section.svg"
          alt="Background"
          className="pointer-events-none absolute inset-0 w-full h-full object-cover opacity-70"
        />

        <div className="absolute transform -translate-x-1/2 top-30 md:top-1/2 left-1/2 flex flex-col items-center">
          <div className="relative">
            <img
              className="w-20 h-20 md:w-40 md:h-40 rounded-full object-cover"
              src="/assets/icons/techhive.png"
              alt="Tech Hive Picture"
            />

            {/* Wrapper for the edit functionality */}
            <div className="absolute top-12 right-0 md:top-25 bg-light rounded-full p-1 md:p-2">
              <img
                className="w-5 h-5 md:w-7 md:h-7 pointer-events-none" // Prevents clicks on the icon itself
                src="/assets/icons/mynaui_edit.png"
                alt="Edit"
              />
            </div>
          </div>
        </div>
      </div>

      <div className="flex flex-col justify-center items-center mt-12 md:mt-22">
        <Text
          variant="h1"
          size="lg"
          bold={false}
          className="md:text-2xl font-semibold text-primary dark:text-custom-white"
        >
          TECHIVE
        </Text>
        <p className="text-secondary text-xs md:text-sm">Admin User</p>
      </div>

      <div className="max-w-7xl mx-auto sm:px-6 lg:px-8">
        <div className="flex flex-col gap-4 mt-5">
          <div className="flex place-self-center bg-light gap-2 p-2 rounded-md text-primary">
            {adminTabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setIsActiveTab(tab.id)}
                className={`flex p-2 items-center gap-2 rounded-md text-xs sm:text-base cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus:ring-gray-700 focus-visible:ring-offset-2 focus-visible:ring-offset-red-300 transition duration-300 ${
                  isActiveTab === tab.id && 'bg-red text-custom-white'
                }`}
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

          <div className="py-8 px-2 md:px-0">
            <div className="lg:p-4 p-0 border border-gray rounded-lg">
              {getContent()}

              {/* Static Pagination */}
              <div className="max-w-7xl mx-auto my-8 flex items-center justify-center">
                <div className="flex items-center space-x-4 ">
                  <Button variant="outline" className="!border-gray-500 !px-3">
                    <MdKeyboardArrowLeft className="w-5 h-5 dark:text-white text-gray-500 hover:!text-white transition-colors" />
                  </Button>

                  <span className="text-gray-600 dark:text-white">1</span>
                  <span className="text-gray-600 dark:text-white">2</span>
                  <span className="text-gray-600 dark:text-white">...</span>
                  <span className="text-gray-600 dark:text-white">4</span>
                  <Button variant="outline" className="!border-gray-500 !px-3">
                    <MdKeyboardArrowRight className="w-5 h-5 dark:text-white text-gray-500 hover:!text-white transition-colors" />
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default AdminDashboard;
