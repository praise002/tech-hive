import { IoFilterOutline } from 'react-icons/io5';
import { MdKeyboardArrowLeft, MdKeyboardArrowRight } from 'react-icons/md';
import { GoPlus, GoArrowDownRight, GoArrowUpRight } from 'react-icons/go';
import { BsToggleOn, BsToggleOff } from 'react-icons/bs';

import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  Line,
  LineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
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
  const [isActiveTab, setIsActiveTab] = useState('manage posts');

  const adminTabs = [
    // {
    //   id: 'manage users',
    //   label: 'Manage users',
    //   icon: <IoPeople className="w-5 h-5" />,
    // },
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

  interface TableCellProps {
    children: React.ReactNode;
    className: string;
  }

  function TableCell({ children, className }: TableCellProps) {
    return (
      <td className={`px-6 whitespace-nowrap lg:table-cell block ${className}`}>
        {children}
      </td>
    );
  }

  interface RoleSpanProps {
    role: string;
  }

  function RoleSpan({ role }: RoleSpanProps) {
    return (
      <span className="lg:px-5 px-2 py-3 rounded-md bg-cream text-orange-dark">
        {role}
      </span>
    );
  }

  interface StatusSpanProps {
    status: string;
  }

  function StatusSpan({ status }: StatusSpanProps) {
    return (
      <span
        className={`lg:px-5 px-2 py-3 rounded-md ${
          status === 'Active' || status === 'Published'
            ? 'bg-mint text-custom-green'
            : 'bg-cream text-red'
        }`}
      >
        {status}
      </span>
    );
  }

  // Remove later since Django comes with admin dashboard(left with reviewer, editor actions)
  // function ManageUsers() {
  //   const users = [
  //     {
  //       id: crypto.randomUUID(),
  //       name: 'Adebayo Samson',
  //       email: 'adebayosamson@gmail.com',
  //       role: 'Subscriber',
  //       status: 'Suspended',
  //     },
  //     {
  //       id: crypto.randomUUID(),
  //       name: 'John Smith',
  //       email: 'johnsmith@gmail.com',
  //       role: 'Admin',
  //       status: 'Active',
  //     },
  //     {
  //       id: crypto.randomUUID(),
  //       name: 'Alice Johnson',
  //       email: 'alice.johnson@example.com',
  //       role: 'Editor',
  //       status: 'Active',
  //     },
  //     {
  //       id: crypto.randomUUID(),
  //       name: 'Bob Williams',
  //       email: 'bob.williams@example.com',
  //       role: 'Reviewer',
  //       status: 'Active',
  //     },
  //     {
  //       id: crypto.randomUUID(),
  //       name: 'Charlie Brown',
  //       email: 'charlie.brown@example.com',
  //       role: 'Subscriber',
  //       status: 'Active',
  //     },
  //     {
  //       id: crypto.randomUUID(),
  //       name: 'Diana Miller',
  //       email: 'diana.miller@example.com',
  //       role: 'Admin',
  //       status: 'Active',
  //     },
  //     {
  //       id: crypto.randomUUID(),
  //       name: 'Ethan Davis',
  //       email: 'ethan.davis@example.com',
  //       role: 'Editor',
  //       status: 'Suspended',
  //     },
  //     {
  //       id: crypto.randomUUID(),
  //       name: 'Fiona Wilson',
  //       email: 'fiona.wilson@example.com',
  //       role: 'Reviewer',
  //       status: 'Active',
  //     },
  //     {
  //       id: crypto.randomUUID(),
  //       name: 'George Moore',
  //       email: 'george.moore@example.com',
  //       role: 'Subscriber',
  //       status: 'Active',
  //     },
  //     {
  //       id: crypto.randomUUID(),
  //       name: 'Hannah Taylor',
  //       email: 'hannah.taylor@example.com',
  //       role: 'Admin',
  //       status: 'Active',
  //     },
  //   ];

  //   const tableHeaders = [
  //     { key: 'name', label: 'Name' },
  //     { key: 'email', label: 'Email' },
  //     { key: 'role', label: 'Role' },
  //     { key: 'status', label: 'Status' },
  //     { key: 'action', label: 'Action' },
  //   ];
  //   return (
  //     <>
  //       <div className="flex justify-between lg:flex-row flex-col gap-y-2 lg:gap-y-0">
  //         <div className="pl-6 pt-8 lg:pt-0">
  //           <button className="flex p-2 items-center gap-2 rounded-md text-xs sm:text-base cursor-pointer bg-red text-custom-white">
  //             <span className="flex-shrink-0">
  //               <GoPlus className="w-5 h-5" />
  //             </span>
  //             <span>Add New User</span>
  //           </button>
  //         </div>
  //         <div className="relative hidden lg:inline-block">
  //           {/* Search Icon */}
  //           <CiSearch className="text-xl absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 dark:text-custom-white" />

  //           {/* Input Field */}
  //           <input
  //             className="appearance-none w-70 dark:text-custom-white border border-gray-500 dark:border-custom-white rounded-md pl-10 pr-3 py-2 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-600 dark:focus-visible:ring-white dark:focus-visible:text-white focus-visible:border-gray-600 dark:focus-visible:border-white"
  //             type="search"
  //             placeholder="Find users by name, email..."
  //           />
  //           <IoFilterOutline className="text-xl absolute right-2 top-1/2 -translate-y-1/2 text-gray-500 dark:text-custom-white" />
  //         </div>
  //       </div>
  //       <div className="mt-4 lg:mt-7">
  //         <table className="min-w-full text-left rtl:text-right">
  //           <caption className="sr-only">
  //             A summary of the user&apos;s table
  //           </caption>
  //           <thead className="hidden lg:table-header-group">
  //             <tr className="font-bold">
  //               {tableHeaders.map((header) => (
  //                 <th key={header.key} scope="col" className="px-6 py-3">
  //                   {header.label}
  //                 </th>
  //               ))}
  //             </tr>
  //           </thead>
  //           <tbody className="lg:text-base lg:divide-y-0 text-sm divide-y divide-gray-200 dark:divide-gray-700">
  //             {users.map((user) => (
  //               <tr key={user.id} className="space-y-2 lg:space-y-0">
  //                 <TableCell className="lg:py-4 pt-2 lg:pt-0">
  //                   {user.name}
  //                 </TableCell>
  //                 <TableCell className="lg:py-4">{user.email}</TableCell>
  //                 <TableCell className="py-4 lg:py-0">
  //                   <RoleSpan role={user.role} />
  //                 </TableCell>
  //                 <TableCell className="py-2 lg:py-0">
  //                   <StatusSpan status={user.status} />
  //                 </TableCell>
  //                 <td className="lg:px-6 lg:py-4 cursor-pointer">...</td>
  //               </tr>
  //             ))}
  //           </tbody>
  //         </table>
  //       </div>
  //     </>
  //   );
  // }

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
        <Articles marginTop={8} showAdminActions={true} />
        <TechJobs />
        <TechEvents />
        <TechTool />
        <ResourceSpotlight />
      </>
    );
  }

  function ManageContent() {
    const [activeRowIndex, setActiveRowIndex] = useState<number | null>(null);

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
                {tableData.map(
                  ({ title, author, date, role, status }, index) => (
                    <tr key={title} className="space-y-2 lg:space-y-0">
                      <TableCell className="lg:py-4 pt-2 lg:pt-0">
                        {title}
                      </TableCell>

                      <TableCell className="lg:py-4">{author}</TableCell>

                      <TableCell className="lg:py-4">{date}</TableCell>
                      <TableCell className="py-4 lg:py-0">
                        <RoleSpan role={role} />
                      </TableCell>
                      <TableCell className="py-2 lg:py-0">
                        <StatusSpan status={status} />
                      </TableCell>
                      <td className="px-6 py-4 cursor-pointer relative">
                        <button
                          type="button"
                          onClick={() =>
                            setActiveRowIndex(
                              activeRowIndex === index ? null : index
                            )
                          }
                        >
                          ...
                        </button>
                        {activeRowIndex === index && (
                          <div className="absolute top-15 right-12">
                            <div className="relative bg-custom-white text-gray-800 gap-2 py-3 px-5 w-50 flex flex-col items-start rounded-md">
                              {/* TODO: UNSURE FOR NOW */}
                              <button>View Details</button>
                              <button>Publish/Reject</button>
                              <button>Provide Feedback</button>

                              <div
                                className="absolute -top-3 right-3 w-4 h-4 bg-white"
                                style={{
                                  clipPath:
                                    'polygon(50% 0%, 0% 100%, 100% 100%)',
                                }}
                              ></div>
                            </div>
                          </div>
                        )}
                      </td>
                    </tr>
                  )
                )}
              </tbody>
            </table>
          </div>
        </div>
      </>
    );
  }

  function Analytics() {
    const deviceTypesData = [
      { name: 'Mobile', value: 400, color: '#a32816' },
      { name: 'Tablet', value: 300, color: '#F58F29' },
      {
        name: 'Desktop',
        value: 200,
        color: '#2EA316',
      },
    ];

    const activeUsersData = [
      { name: 'Mon', registered: 1350, visitors: 900, total: 2250 },
      { name: 'Tue', registered: 1450, visitors: 750, total: 2200 },
      { name: 'Wed', registered: 1200, visitors: 950, total: 2150 },
      { name: 'Thu', registered: 1600, visitors: 600, total: 2200 },
      { name: 'Fri', registered: 1750, visitors: 500, total: 2250 },
      { name: 'Sat', registered: 1000, visitors: 450, total: 1450 },
      { name: 'Sun', registered: 950, visitors: 650, total: 1600 },
    ];

    const topPerformingPostsData = [
      { category: 'Articles', views: 2200, shares: 1400 },
      { category: 'Jobs', views: 1500, shares: 900 },
      { category: 'Events', views: 1800, shares: 1100 },
      { category: 'Featured', views: 2500, shares: 1600 },
    ];

    return (
      <div className="flex flex-col gap-4 px-2 lg:px-0">
        <div className="flex lg:flex-row flex-col justify-between gap-4">
          <div className="flex flex-2 flex-col gap-4">
            <div className="my-6 lg:my-0 flex flex-col lg:flex-row gap-4 justify-between text-primary dark:text-custom-white">
              <div className="flex flex-col items-center gap-y-5 px-8 py-3 rounded-md border border-primary dark:border-gray-200">
                <span className="text-sm">Time on page</span>
                <span className="font-semibold text-2xl">3.2 min</span>
                <p className="inline-flex items-center gap-2 text-xs">
                  <span>
                    <GoArrowUpRight className="text-lime-green" />
                  </span>
                  <span>+1.01% this week</span>
                </p>
              </div>
              <div className="flex flex-col items-center gap-y-5 px-8 py-3 rounded-md border border-primary dark:border-gray-200">
                <span className="text-sm">Bounce rate</span>
                <span className="font-semibold text-2xl">42%</span>
                <p className="inline-flex items-center gap-2 text-xs">
                  <span>
                    <GoArrowUpRight className="text-lime-green" />
                  </span>
                  <span>+0.12% this week</span>
                </p>
              </div>
              <div className="flex flex-col items-center gap-y-5 px-8 py-3 rounded-md border border-primary dark:border-gray-200">
                <span className="text-sm">Load speed</span>
                <span className="font-semibold text-2xl">1.0 min</span>
                <p className="inline-flex items-center gap-2 text-xs">
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
          <div className="flex flex-1 flex-col items-center gap-y-5 px-8 py-3 rounded-md border border-primary dark:border-gray-200">
            <div className="flex justify-between gap-4">
              <Text
                variant="h3"
                bold={false}
                className="font-semibold mb-1 text-gray-900 dark:text-custom-white"
              >
                Device types
              </Text>

              <form>
                <select className="dark:text-custom-white dark:bg-dark text-sm py-1 px-2 border border-gray-300 rounded-md focus-visible:outline-none focus-visible:ring-2 focus:ring-gray-700">
                  <option value="">Weekly</option>
                  <option value="monthly">Monthly</option>
                </select>
              </form>
            </div>
            {/* Width and height has to be set on a div for the piechart to display */}
            <div className="w-full h-[200px]">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={deviceTypesData}
                    nameKey="name" // property e.g Mobile
                    dataKey="value" // value: 400
                    innerRadius="40%" // creates a donut hole
                    outerRadius="70%" // sets the outer boundary
                    cx="50%" // cx and cy centres the pie chart
                    cy="50%"
                    paddingAngle={3} // Adds a 3-degree gap between slices
                  >
                    {deviceTypesData.map((entry) => (
                      <Cell
                        fill={entry.color} // Sets the fill color for each slice
                        stroke={entry.color} // Sets the border color for each slice
                        key={entry.value}
                      />
                    ))}
                  </Pie>
                  <Tooltip />
                  <Legend
                    verticalAlign="bottom"
                    align="center"
                    layout="horizontal"
                    iconSize={15}
                    iconType="circle"
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
        <div className="flex flex-col lg:flex-row gap-4">
          <div className="flex flex-1 flex-col gap-y-5 px-8 py-3 rounded-md border border-primary dark:border-gray-200">
            <div className="flex justify-between">
              <Text
                variant="h3"
                bold={false}
                className="font-semibold mb-1 text-gray-900 dark:text-custom-white"
              >
                Active users overview
              </Text>
              <form>
                <select className="dark:text-custom-white text-sm dark:bg-dark py-1 px-2  border border-gray-300 rounded-md focus-visible:outline-none focus-visible:ring-2 focus:ring-gray-700">
                  <option value="">Weekly</option>
                  <option value="monthly">Monthly</option>
                </select>
              </form>
            </div>
            <div className="w-full h-[250px]">
              <ResponsiveContainer width="100%" height="100%">
                {/* creates space around the chart for axes and labels */}
                <LineChart
                  data={activeUsersData}
                  margin={{
                    top: 5,
                    right: 30,
                    left: 20,
                    bottom: 5,
                  }}
                >
                  {/* Creates the background grid lines with a dash pattern and light opacity */}
                  <CartesianGrid strokeDasharray="3 3" opacity={0.1} />
                  <XAxis dataKey="name" /> {/* Displays days of the week */}
                  {/* Automatically scales to fit your data values (450 to 2250) */}
                  <YAxis />
                  <Tooltip />
                  <Legend
                    verticalAlign="bottom"
                    align="center"
                    layout="horizontal"
                    iconSize={15}
                    iconType="circle"
                    formatter={(value) => {
                      // Map data keys to custom labels
                      const customLabels: { [key: string]: string } = {
                        registered: 'Registered Users',
                        visitors: 'Visitors',
                        total: 'Total Active Users',
                      };

                      // Return the custom label if it exists, otherwise return the original value
                      return (
                        <span className="text-xs lg:text-sm">
                          {customLabels[value] || value}
                        </span>
                      );
                    }}
                  />
                  <Line
                    type="monotone" // creates smooth, curved lines between points
                    dataKey="registered"
                    stroke="#a32816" // Sets the line color (using your theme colors)
                    strokeWidth={2} // Makes the lines thicker for better visibility
                    activeDot={{ r: 8 }} // makes the active dot larger when hovering
                  />
                  <Line
                    type="monotone"
                    dataKey="visitors"
                    stroke="#F58F29"
                    strokeWidth={2}
                  />
                  <Line
                    type="monotone"
                    dataKey="total"
                    stroke="#2EA316"
                    strokeWidth={2}
                  />
                </LineChart>
              </ResponsiveContainer>
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
                <select className="dark:text-custom-white text-sm dark:bg-dark py-1 px-2  border border-gray-300 rounded-md focus-visible:outline-none focus-visible:ring-2 focus:ring-gray-700">
                  <option value="">Weekly</option>
                  <option value="monthly">Monthly</option>
                </select>
              </form>
            </div>

            <div className="w-full h-[250px]">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart
                  data={topPerformingPostsData}
                  margin={{
                    top: 5,
                    right: 30,
                    left: 20,
                    bottom: 5,
                  }}
                >
                  <CartesianGrid strokeDasharray="3 3" opacity={0.1} />
                  <XAxis dataKey="category" />
                  <YAxis domain={[0, 3000]} />
                  <Tooltip />
                  <Legend
                    verticalAlign="bottom"
                    align="center"
                    layout="horizontal"
                    iconSize={15}
                    iconType="circle"
                  />
                  <Bar
                    dataKey="views"
                    name="Views"
                    fill="#a32816"
                    barSize={30}
                  />
                  <Bar
                    dataKey="shares"
                    name="Shares"
                    fill="#F58F29"
                    barSize={30}
                  />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // ONLY ADMIN
  function Settings() {
    const [isToggle, setIsToggle] = useState(false);

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

          {/* <div>
            <label htmlFor="">Password</label>
            <div className="relative">
              <input
                type="text"
                className="appearance-none block w-full px-4 py-2 border border-gray-300 rounded-md focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-800 focus-visible:border-gray-800"
                value="*******"
              />
              <img
                className="w-5 h-5 absolute top-1/2 right-3 -translate-y-1/2 cursor-pointer"
                src="/assets/icons/streamline_invisible-2.png"
                alt="An icon to toggle the visibility of password"
              />
            </div>
          </div> */}

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

          {/* <div className="">
            <label htmlFor="" className="block">
              Color
            </label>
            <select className="dark:text-custom-white dark:bg-dark py-2 px-4 border border-gray-300 rounded-md focus-visible:outline-none focus-visible:ring-2 focus:ring-gray-700 w-full">
              <option value="">Pink</option>
              <option value="purple">Purple</option>
            </select>
          </div> */}

          <div className="">
            <label htmlFor="themeColor" className="block">
              Color
            </label>
            <div className="border border-gray-300 rounded-md">
              <input
                type="color"
                id="themeColor"
                value="#a32816"
                className="w-20 h-10 p-1 cursor-pointer"
              />
            </div>
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
            <button
              type="button"
              onClick={() => setIsToggle(!isToggle)}
              aria-pressed={isToggle}
              aria-label="Toggle two-factor authentication"
            >
              {isToggle ? <BsToggleOn /> : <BsToggleOff />}
            </button>
          </div>

          <Button className="w-full">Save Changes</Button>
        </form>
      </div>
    );
  }

  function getContent() {
    switch (isActiveTab) {
      // case 'manage users':
      //   return <ManageUsers />;
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

          <div className="py-8">
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
