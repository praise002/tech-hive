import { IoPeople } from 'react-icons/io5';
import { IoFilterOutline } from 'react-icons/io5';
import { MdKeyboardArrowLeft, MdKeyboardArrowRight } from 'react-icons/md';
import { GoPlus, GoArrowDownRight, GoArrowUpRight } from 'react-icons/go';
import { BsToggleOn, BsToggleOff } from 'react-icons/bs';

import Text from '../../components/common/Text';
import {
  MdArticle,
  MdLibraryBooks,
  MdAnalytics,
  MdSettings,
} from 'react-icons/md';

import { CiSearch } from 'react-icons/ci';
import Button from '../../components/common/Button';
import { useState } from 'react';

const users = [
  {
    id: crypto.randomUUID(),
    name: 'Adebayo Samson',
    email: 'adebayosamson@gmail.com',
    role: 'Subscriber',
    status: 'Suspended',
  },
  {
    id: crypto.randomUUID(),
    name: 'John Smith',
    email: 'johnsmith@gmail.com',
    role: 'Admin',
    status: 'Active',
  },
  {
    id: crypto.randomUUID(),
    name: 'Alice Johnson',
    email: 'alice.johnson@example.com',
    role: 'Editor',
    status: 'Active',
  },
  {
    id: crypto.randomUUID(),
    name: 'Bob Williams',
    email: 'bob.williams@example.com',
    role: 'Reviewer',
    status: 'Active',
  },
  {
    id: crypto.randomUUID(),
    name: 'Charlie Brown',
    email: 'charlie.brown@example.com',
    role: 'Subscriber',
    status: 'Active',
  },
  {
    id: crypto.randomUUID(),
    name: 'Diana Miller',
    email: 'diana.miller@example.com',
    role: 'Admin',
    status: 'Active',
  },
  {
    id: crypto.randomUUID(),
    name: 'Ethan Davis',
    email: 'ethan.davis@example.com',
    role: 'Editor',
    status: 'Suspended',
  },
  {
    id: crypto.randomUUID(),
    name: 'Fiona Wilson',
    email: 'fiona.wilson@example.com',
    role: 'Reviewer',
    status: 'Active',
  },
  {
    id: crypto.randomUUID(),
    name: 'George Moore',
    email: 'george.moore@example.com',
    role: 'Subscriber',
    status: 'Active',
  },
  {
    id: crypto.randomUUID(),
    name: 'Hannah Taylor',
    email: 'hannah.taylor@example.com',
    role: 'Admin',
    status: 'Active',
  },
];

function AdminDashboard() {
  const [isActiveTab, setIsActiveTab] = useState('manage users');

  const adminTabs = [
    {
      id: 'manage users',
      label: 'Manage users',
      icon: <IoPeople className="w-5 h-5" />,
    },
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
    {
      id: 'settings',
      label: 'Settings',
      icon: <MdSettings className="w-5 h-5" />,
    },
  ];

  function ManageUsers() {
    return (
      <>
        <div className="flex justify-between">
          <button className="flex p-2 items-center gap-2 rounded-md text-xs sm:text-base cursor-pointer bg-red text-custom-white">
            <span className="flex-shrink-0">
              <GoPlus className="w-5 h-5" />
            </span>
            <span>Add New User</span>
          </button>
          <div className="relative">
            {/* Search Icon */}
            <CiSearch className="text-xl absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 dark:text-custom-white" />

            {/* Input Field */}
            <input
              className="appearance-none w-70 dark:text-custom-white border border-gray-500 dark:border-custom-white rounded-md pl-10 pr-3 py-2 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-600 dark:focus-visible:ring-white dark:focus-visible:text-white focus-visible:border-gray-600 dark:focus-visible:border-white"
              type="search"
              placeholder="Find users by name, email..."
            />
            <IoFilterOutline className="text-xl absolute right-2 top-1/2 -translate-y-1/2 text-gray-500 dark:text-custom-white" />
          </div>
        </div>
        <div className="mt-7">
          <table className="w-full text-left rtl:text-right">
            <caption className="sr-only">
              A summary of the user&apos;s table
            </caption>
            <thead>
              <tr className="font-bold">
                <th scope="col" className="px-6 py-3">
                  Name
                </th>
                <th scope="col" className="px-6 py-3">
                  Email
                </th>
                <th scope="col" className="px-6 py-3">
                  Role
                </th>
                <th scope="col" className="px-6 py-3">
                  Status
                </th>
                <th scope="col" className="px-6 py-3">
                  Action
                </th>
              </tr>
            </thead>
            <tbody>
              {users.map((user) => (
                <tr key={user.id}>
                  <td className="px-6 py-4">{user.name}</td>
                  <td className="px-6 py-4">{user.email}</td>
                  <td className="px-6 py-4">
                    <span className="px-5 py-3 rounded-md bg-cream text-orange-dark">
                      {user.role}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <span
                      className={`px-5 py-3 rounded-md ${
                        user.status === 'Active'
                          ? 'bg-mint text-custom-green'
                          : 'bg-cream text-red'
                      }`}
                    >
                      {user.status}
                    </span>
                  </td>
                  <td className="px-6 py-4">...</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </>
    );
  }
  function ManagePosts() {
    return <>Manage posts</>;
  }
  function ManageContent() {
    return <>Manage content</>;
  }
  function Analytics() {
    return <>Analytics</>;
  }
  function Settings() {
    return <>Settings</>;
  }

  function getContent() {
    switch (isActiveTab) {
      case 'manage users':
        return <ManageUsers />;
      case 'manage posts':
        return <ManagePosts />;
      case 'manage content':
        return <ManageContent />;
      case 'analytics':
        return <Analytics />;
      case 'settings':
        return <Settings />;
      default:
        return null;
    }
  }

  return (
    <div className="dark:text-custom-white">
      <div className="relative mt-12 bg-gradient-to-r from-coral/50 to-peach py-10 px-7 sm:py-20 sm:px-14 h-40">
        {/* ✅ SVG Background */}
        <img
          src="/src/assets/hero-section.svg"
          alt="Background"
          className="pointer-events-none absolute inset-0 w-full h-full object-cover opacity-70"
        />

        <div className="absolute transform -translate-x-1/2 top-30 md:top-1/2 left-1/2 flex flex-col items-center">
          <div className="relative">
            <img
              className="w-20 h-20 md:w-40 md:h-40 rounded-full object-cover"
              src="/src/assets/icons/techhive.png"
              alt="Tech Hive Picture"
            />

            {/* Wrapper for the edit functionality */}
            <div className="absolute top-12 right-0 md:top-25 bg-light rounded-full p-1 md:p-2">
              <img
                className="w-5 h-5 md:w-7 md:h-7 pointer-events-none" // Prevents clicks on the icon itself
                src="/src/assets/icons/mynaui_edit.png"
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
        <div className="flex flex-col gap-4 items-center mt-5">
          <div className="flex bg-light gap-2 p-2 rounded-md text-primary ">
            {adminTabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setIsActiveTab(tab.id)}
                className={`flex p-2 items-center gap-2 rounded-md text-xs sm:text-base cursor-pointer ${
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

          <div className="py-8 flex justify-center">
            <div className="dark:text-custom-white">
              <div className="p-4 border border-gray rounded-lg">
                {getContent()}

                {/* Static Pagination */}
                <div className="max-w-7xl mx-auto mt-8 flex items-center justify-center">
                  <div className="flex items-center space-x-4 ">
                    <Button
                      variant="outline"
                      className="!border-gray-500 !px-3"
                    >
                      <MdKeyboardArrowLeft className="w-5 h-5 dark:text-white text-gray-500 hover:!text-white transition-colors" />
                    </Button>

                    <span className="text-gray-600 dark:text-white">1</span>
                    <span className="text-gray-600 dark:text-white">2</span>
                    <span className="text-gray-600 dark:text-white">...</span>
                    <span className="text-gray-600 dark:text-white">4</span>
                    <Button
                      variant="outline"
                      className="!border-gray-500 !px-3"
                    >
                      <MdKeyboardArrowRight className="w-5 h-5 dark:text-white text-gray-500 hover:!text-white transition-colors" />
                    </Button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div></div>
    </div>
  );
}

export default AdminDashboard;
