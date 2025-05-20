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
import Articles from '../../components/sections/Articles';
import TechJobs from '../../components/sections/TechJobs';
import TechEvents from '../../components/sections/TechEvents';
import TechTool from '../../components/sections/TechTool';
import ResourceSpotlight from '../../components/sections/ResourceSpotlight';

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

    const tableHeaders = [
      { key: 'name', label: 'Name' },
      { key: 'email', label: 'Email' },
      { key: 'role', label: 'Role' },
      { key: 'status', label: 'Status' },
      { key: 'action', label: 'Action' },
    ];
    return (
      <>
        <div className="flex justify-between lg:flex-row flex-col gap-y-2 lg:gap-y-0">
          <div className="pl-6 pt-8 lg:pt-0">
            <button className="flex p-2 items-center gap-2 rounded-md text-xs sm:text-base cursor-pointer bg-red text-custom-white">
              <span className="flex-shrink-0">
                <GoPlus className="w-5 h-5" />
              </span>
              <span>Add New User</span>
            </button>
          </div>
          <div className="relative hidden lg:inline-block">
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
        <div className="mt-4 lg:mt-7">
          <table className="min-w-full text-left rtl:text-right">
            <caption className="sr-only">
              A summary of the user&apos;s table
            </caption>
            <thead className="hidden lg:table-header-group">
              <tr className="font-bold">
                {tableHeaders.map((header) => (
                  <th key={header.key} scope="col" className="px-6 py-3">
                    {header.label}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="lg:text-base lg:divide-y-0 text-sm divide-y divide-gray-200 dark:divide-gray-700">
              {users.map((user) => (
                <tr key={user.id} className="space-y-2 lg:space-y-0">
                  <td className="px-6 lg:py-4 pt-2 whitespace-nowrap lg:table-cell block">
                    {user.name}
                  </td>
                  <td className="px-6 lg:py-4 whitespace-nowrap lg:table-cell block">
                    {user.email}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap lg:table-cell block">
                    <span className="lg:px-5 px-2 py-3 rounded-md bg-cream text-orange-dark">
                      {user.role}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap lg:table-cell block">
                    <span
                      className={`lg:px-5 px-2 py-3 rounded-md ${
                        user.status === 'Active'
                          ? 'bg-mint text-custom-green'
                          : 'bg-cream text-red'
                      }`}
                    >
                      {user.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 cursor-pointer">...</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </>
    );
  }

  function ManagePosts() {
    return (
      <>
        <div className="flex justify-between lg:flex-row flex-col gap-y-2 lg:gap-y-0">
          <div className="pl-6 pt-8 lg:pt-0">
            <button className="flex p-2 items-center gap-2 rounded-md text-xs sm:text-base cursor-pointer bg-red text-custom-white">
              <span className="flex-shrink-0">
                <GoPlus className="w-5 h-5" />
              </span>
              <span>Add New Post</span>
            </button>
          </div>
          <div className="relative hidden lg:inline-block">
            {/* Search Icon */}
            <CiSearch className="text-xl absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 dark:text-custom-white" />

            {/* Input Field */}
            <input
              className="appearance-none w-70 dark:text-custom-white border border-gray-500 dark:border-custom-white rounded-md pl-10 pr-3 py-2 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-600 dark:focus-visible:ring-white dark:focus-visible:text-white focus-visible:border-gray-600 dark:focus-visible:border-white"
              type="search"
              placeholder="Find posts by title..."
            />
            <IoFilterOutline className="text-xl absolute right-2 top-1/2 -translate-y-1/2 text-gray-500 dark:text-custom-white" />
          </div>
        </div>
        <Articles />
        <TechJobs />
        <TechEvents />
        <TechTool />
        <ResourceSpotlight />
      </>
    );
  }

  function ManageContent() {
    const contentStats = [
      { label: 'All posts', count: 24 },
      { label: 'Drafts', count: 2 },
      { label: 'Submitted', count: 7 },
      { label: 'Published', count: 18 },
      { label: 'Rejected', count: 2 },
    ];

    const tableHeaders = [
      { key: 'title', label: 'Post Title' },
      { key: 'author', label: 'Author' },
      { key: 'date', label: 'Date' },
      { key: 'role', label: 'Role' },
      { key: 'status', label: 'Status' },
      { key: 'action', label: 'Action' },
    ];

    const tableData = [
      {
        title: 'The Future of UI/UX: Trends...',
        author: 'TECHIVE',
        date: '29/12/24',
        role: 'Admin',
        status: 'Published',
      },
      {
        title: 'The rise of blockchain in Re...',
        author: 'Adeyinka Favor',
        date: '26/12/24',
        role: 'Contributor',
        status: 'Published',
      },
      {
        title: 'AI-Powered Marketing Strategies',
        author: 'Jane Doe',
        date: '20/12/24',
        role: 'Editor',
        status: 'Rejected',
      },
      {
        title: 'Cybersecurity Best Practices',
        author: 'Robert Smith',
        date: '15/12/24',
        role: 'Reviewer',
        status: 'Rejected',
      },
      {
        title: 'Cloud Computing Trends',
        author: 'Alice Johnson',
        date: '10/12/24',
        role: 'Admin',
        status: 'Published',
      },
      {
        title: 'The Impact of IoT on Industries',
        author: 'David Lee',
        date: '05/12/24',
        role: 'Contributor',
        status: 'Published',
      },
      {
        title: 'Data Science for Beginners',
        author: 'Emily White',
        date: '01/12/24',
        role: 'Editor',
        status: 'Rejected',
      },
      {
        title: 'Mobile App Development Tips',
        author: 'Michael Brown',
        date: '25/11/24',
        role: 'Reviewer',
        status: 'Rejected',
      },
      {
        title: 'The Future of Work',
        author: 'Sarah Green',
        date: '20/11/24',
        role: 'Admin',
        status: 'Published',
      },
      {
        title: 'Ethical Considerations in AI',
        author: 'Kevin Black',
        date: '15/11/24',
        role: 'Contributor',
        status: 'Published',
      },
    ];

    return (
      <>
        <div>
          <div className="my-6 lg:my-0 mx-6 flex flex-col lg:flex-row gap-4 justify-between text-primary dark:text-custom-white">
            {contentStats.map(({ label, count }) => (
              <div
                key={label}
                className="flex flex-col items-center gap-y-5 px-8 py-3 rounded-md border border-primary dark:border-gray-200"
              >
                <span className="font-medium">{label}</span>
                <span className="font-semibold">{count}</span>
              </div>
            ))}
          </div>
          <div>
            <div className="relative hidden lg:flex lg:justify-end my-6 mr-6">
              <div className="relative">
                {/* Search Icon */}
                <CiSearch className="text-xl absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 dark:text-custom-white" />

                {/* Input Field */}
                <input
                  className="appearance-none w-70 dark:text-custom-white border border-gray-500 dark:border-custom-white rounded-md pl-10 pr-3 py-2 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-600 dark:focus-visible:ring-white dark:focus-visible:text-white focus-visible:border-gray-600 dark:focus-visible:border-white"
                  type="search"
                  placeholder="Find posts by title..."
                />
                <IoFilterOutline className="text-xl absolute right-2 top-1/2 -translate-y-1/2 text-gray-500 dark:text-custom-white" />
              </div>
            </div>
          </div>
          <div>
            <table className="min-w-full text-left rtl:text-right">
              <caption className="sr-only">
                A summary of the content&apos;s table
              </caption>
              <thead className="hidden lg:table-header-group">
                <tr className="font-bold">
                  {tableHeaders.map(({ key, label }) => (
                    <th key={key} scope="col" className="px-6 py-3">
                      {label}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="lg:text-base lg:divide-y-0 text-sm divide-y divide-gray-200 dark:divide-gray-700">
                {tableData.map(({ title, author, date, role, status }) => (
                  <tr key={title} className="space-y-2 lg:space-y-0">
                    <td className="px-6 lg:py-4 pt-2 whitespace-nowrap lg:table-cell block">
                      {title}
                    </td>
                    <td className="px-6 lg:py-4 whitespace-nowrap lg:table-cell block">
                      {author}
                    </td>
                    <td>{date}</td>
                    <td className="px-6 py-4 whitespace-nowrap lg:table-cell block">
                      <span className="lg:px-5 px-2 py-3 rounded-md bg-cream text-orange-dark">
                        {role}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap lg:table-cell block">
                      <span
                        className={`lg:px-5 px-2 py-3 rounded-md ${
                          status === 'Published'
                            ? 'bg-mint text-custom-green'
                            : 'bg-cream text-red'
                        }`}
                      >
                        {status}
                      </span>
                    </td>
                    <td className="px-6 py-4 cursor-pointer">...</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </>
    );
  }
  function Analytics() {
    return (
      <div className="flex flex-col gap-4 px-2 lg:px-0">
        <div className="flex lg:flex-row flex-col justify-between gap-4">
          <div className="flex flex-col gap-4">
            <div className="my-6 lg:my-0 flex flex-col lg:flex-row gap-4 justify-between text-primary dark:text-custom-white">
              <div className="flex flex-col items-center gap-y-5 px-8 py-3 rounded-md border border-primary dark:border-gray-200">
                <span className="text-sm">Time on page</span>
                <span className="font-semibold text-2xl">3.2 min</span>
                <p className="inline-flex items-center gap-2 text-sm">
                  <span>
                    <GoArrowUpRight className="text-lime-green" />
                  </span>
                  <span>+1.01% this week</span>
                </p>
              </div>
              <div className="flex flex-col items-center gap-y-5 px-8 py-3 rounded-md border border-primary dark:border-gray-200">
                <span className="text-sm">Bounce rate</span>
                <span className="font-semibold text-2xl">42%</span>
                <p className="inline-flex items-center gap-2 text-sm">
                  <span>
                    <GoArrowUpRight className="text-lime-green" />
                  </span>
                  <span>+0.12% this week</span>
                </p>
              </div>
              <div className="flex flex-col items-center gap-y-5 px-8 py-3 rounded-md border border-primary dark:border-gray-200">
                <span className="text-sm">Load speed</span>
                <span className="font-semibold text-2xl">1.0 min</span>
                <p className="inline-flex items-center gap-2 text-sm">
                  <span>
                    <GoArrowDownRight className="text-red" />
                  </span>
                  <span>-1.01% this week</span>
                </p>
              </div>
            </div>
            <div className="flex h-full justify-center flex-col items-center gap-y-5 px-8 py-3 rounded-md border border-primary dark:border-gray-200">
              <div className="flex justify-between w-full">
                <h3>Top Hashtag Performance</h3>
                <p>...</p>
              </div>
              <div className="flex justify-between w-full">
                <div className="flex">
                  <p className="text-cyan-light">#</p>
                  <h3>Crypto</h3>
                </div>
                <p>1.5k Engagements</p>
              </div>
            </div>
          </div>
          <div className="flex flex-col items-center gap-y-5 px-8 py-3 rounded-md border border-primary dark:border-gray-200">
            <div className="flex justify-between gap-4">
              <Text
                variant="h3"
                bold={false}
                className="font-semibold mb-1 text-gray-900 dark:text-custom-white"
              >
                Device types
              </Text>

              <form>
                <select className="dark:text-custom-white dark:bg-dark text-sm py-2 px-4 border border-gray-300 rounded-md focus-visible:outline-none focus-visible:ring-2 focus:ring-gray-700">
                  <option value="">Weekly</option>
                  <option value="monthly">Monthly</option>
                </select>
              </form>
            </div>
            <div>
              <img src="/src/assets/images/Chart 1.png" alt="" />
            </div>
            <div className="flex gap-4">
              <div className="flex items-center gap-2">
                <p className="rounded-full w-2 h-2 bg-red"></p>
                <p>Mobile</p>
              </div>
              <div className="flex items-center gap-2">
                <p className="rounded-full w-2 h-2 bg-honey"></p>
                <p>Tablet</p>
              </div>
              <div className="flex items-center gap-2">
                <p className="rounded-full w-2 h-2 bg-custom-green"></p>
                <p>Desktop</p>
              </div>
            </div>
          </div>
        </div>
        <div className="flex flex-col lg:flex-row gap-4">
          <div className="flex flex-1 flex-col  gap-y-5 px-8 py-3 rounded-md border border-primary dark:border-gray-200">
            <div className="flex justify-between">
              <Text
                variant="h3"
                bold={false}
                className="font-semibold mb-1 text-gray-900 dark:text-custom-white"
              >
                Active users overview
              </Text>
              <form>
                <select className="dark:text-custom-white text-sm dark:bg-dark py-2 px-4 border border-gray-300 rounded-md focus-visible:outline-none focus-visible:ring-2 focus:ring-gray-700">
                  <option value="">Weekly</option>
                  <option value="monthly">Monthly</option>
                </select>
              </form>
            </div>
            <div>
              <img src="/src/assets/images/chart-2.png" alt="" />
            </div>
            <div className="flex gap-4">
              <div className="flex items-center gap-2">
                <p className="rounded-full w-2 h-2 bg-red"></p>
                <p>Registered Users</p>
              </div>
              <div className="flex items-center gap-2">
                <p className="rounded-full w-2 h-2 bg-honey"></p>
                <p>Visitors</p>
              </div>
              <div className="flex items-center gap-2">
                <p className="rounded-full w-2 h-2 bg-custom-green"></p>
                <p>Total Active Users</p>
              </div>
            </div>
          </div>
          <div className="flex flex-col flex-1 gap-y-5 px-8 py-3 rounded-md border border-primary dark:border-gray-200">
            <div className="flex justify-between">
              <Text
                variant="h3"
                bold={false}
                className="font-semibold mb-1 text-gray-900 dark:text-custom-white"
              >
                Top Performing Post
              </Text>
              <form>
                <select className="dark:text-custom-white text-sm dark:bg-dark py-2 px-4 border border-gray-300 rounded-md focus-visible:outline-none focus-visible:ring-2 focus:ring-gray-700">
                  <option value="">Weekly</option>
                  <option value="monthly">Monthly</option>
                </select>
              </form>
            </div>

            <div>
              <img src="/src/assets/images/chart-3.png" alt="" />
            </div>
            <div className="flex gap-4 justify-center">
              <div className="flex items-center gap-2">
                <p className="rounded-full w-2 h-2 bg-red"></p>
                <p>Views</p>
              </div>
              <div className="flex items-center gap-2">
                <p className="rounded-full w-2 h-2 bg-honey"></p>
                <p>Shares</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  function Settings() {
    return (
      <div className="p-8">
        <form className="space-y-6">
          <div className="">
            <label htmlFor="">Site Name</label>
            <input
              type="text"
              className="appearance-none block w-full px-4 py-2 border border-gray-300 rounded-md focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-800 focus-visible:border-gray-800"
              value="TECHIVE"
            />
          </div>

          <div>
            <label htmlFor="">Password</label>
            <div className="relative">
              <input
                type="text"
                className="appearance-none block w-full px-4 py-2 border border-gray-300 rounded-md focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-800 focus-visible:border-gray-800"
                value="*******"
              />
              <img
                className="w-5 h-5 absolute top-1/2 right-3 -translate-y-1/2 cursor-pointer"
                src="/src/assets/icons/streamline_invisible-2.png"
                alt="An icon to toggle the visibility of password"
              />
            </div>
          </div>

          <div>
            <label htmlFor="">Tagline</label>
            <input
              type="text"
              className="appearance-none block w-full px-4 py-2 border border-gray-300 rounded-md focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-800 focus-visible:border-gray-800"
            />
          </div>

          <div className="">
            <label htmlFor="" className="block">
              Default Language
            </label>
            <select className="dark:text-custom-white dark:bg-dark py-2 px-4 border border-gray-300 rounded-md focus-visible:outline-none focus-visible:ring-2 focus:ring-gray-700 w-full">
              <option value="">English</option>
              <option value="french">French</option>
            </select>
          </div>

          <div className="">
            <label htmlFor="" className="block">
              Color
            </label>
            <select className="dark:text-custom-white dark:bg-dark py-2 px-4 border border-gray-300 rounded-md focus-visible:outline-none focus-visible:ring-2 focus:ring-gray-700 w-full">
              <option value="">Pink</option>
              <option value="purple">Purple</option>
            </select>
          </div>

          <div className="">
            <label htmlFor="" className="block">
              Typography
            </label>
            <select className="dark:text-custom-white dark:bg-dark py-2 px-4 border border-gray-300 rounded-md focus-visible:outline-none focus-visible:ring-2 focus:ring-gray-700 w-full">
              <option value="">Inter</option>
              <option value="roboto">Roboto</option>
            </select>
          </div>

          <div className="flex items-center justify-between">
            <p>Enable Two-factor Authentication</p>
            <p>
              <BsToggleOn />
            </p>
          </div>

          <Button className="w-full">Save Changes</Button>
        </form>
      </div>
    );
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
        <div className="flex flex-col gap-4  mt-5">
          <div className="flex place-self-center bg-light gap-2 p-2 rounded-md text-primary">
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

          <div className="py-8">
            <div className=" lg:p-4 p-0 border border-gray rounded-lg">
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
