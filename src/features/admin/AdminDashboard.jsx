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

function AdminDashboard() {
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
  return (
    <div className="pt-30 dark:text-custom-white ">
      <div className="relative mt-12 bg-gradient-to-r from-coral/50 to-peach py-10 px-7 sm:py-20 sm:px-14 overflow-hidden h-40">
        {/* ✅ SVG Background */}
        <img
          src="/src/assets/hero-section.svg"
          alt="Background"
          className="pointer-events-none absolute inset-0 w-full h-full object-cover opacity-70"
        />
      </div>

      <svg
        width="151"
        height="150"
        viewBox="0 0 151 150"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        xmlnsXlink="http://www.w3.org/1999/xlink"
      >
        <circle
          cx="75.1309"
          cy="75"
          r="74.6246"
          fill="url(#pattern0_871_137)"
          stroke="#A32816"
          strokeWidth="0.750788"
        />
        <defs>
          <pattern
            id="pattern0_871_137"
            patternContentUnits="objectBoundingBox"
            width="1"
            height="1"
          >
            <use xlinkHref="#image0_871_137" transform="scale(0.00135135)" />
          </pattern>
          <image
            id="image0_871_137"
            width="740"
            height="740"
            preserveAspectRatio="none"
            xlinkHref="data:image/jpeg;base64,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AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQQwwwwwwgAAAAQ44wwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAXnHHHHH4EAAReEEEx0AAAAAAAAAAAAAAAAAAAAAAAAAAAABSoBegBuEAASYMAAAD0AAAAAAAAAAAAAAAAAAAAAAAAAAAABSpqMEaAAAFAAAAoAD0AAAAAAAAAAAAAAAAAAAAAAAAAAAABSqEUqAAAnoAAA4EAD0AAAAAAAAAAAAAAAAAAAAAAAAAAAABSoEIAABCAAABuIAAD0AAAAAAAAAAAAAAAAAAAAAAAAAAAABC4oAAB1AAAAAAAAAH4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAKoAABBcAIAAIIIILfQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEBEGmQEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAUAAOICPIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAACEAAAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAWkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQEAAAQsIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAACAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABEAAQAAAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABQAEKAAAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAFOEAAAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBKMMMMMUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABHDDDDDCIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA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"
          />
        </defs>
      </svg>

      <div className="absolute top-12 right-0 md:top-25 bg-light rounded-full p-1 md:p-2">
        <img
          className="w-5 h-5 md:w-7 md:h-7 pointer-events-none" // Prevents clicks on the icon itself
          src="/src/assets/icons/mynaui_edit.png"
          alt="Edit"
        />
      </div>

      <Text
        variant="h3"
        size="lg"
        bold={false}
        className="font-semibold text-primary dark:text-custom-white"
      >
        TECHIVE
      </Text>
      <p className="text-secondary">Admin User</p>

      <div className="flex bg-light gap-2 p-2 rounded-md">
        {adminTabs.map((tab) => (
          <button
            key={tab.id}
            // onClick={() => setIsActiveTab(tab.id)}
            // className={`flex p-2 items-center gap-2 rounded-md text-xs sm:text-base cursor-pointer ${
            //   isActiveTab === tab.id && 'bg-red text-custom-white'
            // }`}
            className="flex p-2 items-center gap-2 rounded-md text-xs sm:text-base cursor-pointer bg-red text-custom-white"
          >
            <span className="flex-shrink-0">{tab.icon}</span>
            <span
            // className={`${
            //   isActiveTab == tab.id ? 'inline' : 'hidden md:inline'
            // }`}
            >
              {tab.label}
            </span>
          </button>
        ))}
      </div>
      <div>
        <div>
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
              className="w-70 dark:text-custom-white border border-gray-500 dark:border-custom-white rounded-md pl-10 pr-3 py-2 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-600 dark:focus-visible:ring-white dark:focus-visible:text-white focus-visible:border-gray-600 dark:focus-visible:border-white"
              type="search"
              placeholder="Find users by name, email..."
            />
            <IoFilterOutline className="text-xl absolute right-205 top-1/2 -translate-y-1/2 text-gray-500 dark:text-custom-white" />
          </div>
        </div>
        <div>
          <table>
            <caption>A summary of the user&apos;s table</caption>
            <thead>
              <tr>
                <th scope="col">Name</th>
                <th scope="col">Email</th>
                <th scope="col">Role</th>
                <th scope="col">Status</th>
                <th scope="col">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Adebayo Samson</td>
                <td>adebayosamson@gmail.com</td>
                <td>Contributor</td>
                <td>Suspended</td>
                <td>...</td>
              </tr>
              <tr>
                <td>John Smith</td>
                <td>johnsmith@gmail.com</td>
                <td>Contributor</td>
                <td>Active</td>
              </tr>
            </tbody>
          </table>
        </div>
        {/* Static Pagination */}
        <div className="max-w-7xl mx-auto mt-8 flex items-center justify-center">
          <div className="flex items-center space-x-2">
            <Button variant="outline" className="!border-gray-500">
              <MdKeyboardArrowLeft className="w-5 h-5 text-gray-500" />
            </Button>

            <span className="text-gray-600">1</span>
            <span className="text-gray-600">2</span>
            <span className="text-gray-600">...</span>
            <span className="text-gray-600">4</span>
            <Button variant="outline" className="!border-gray-500">
              <MdKeyboardArrowRight className="w-5 h-5 text-gray-500" />
            </Button>
          </div>
        </div>
      </div>

      {/* Content tab */}
      <div>
        <div>
          <div>
            <span>All posts</span>
            <span>24</span>
          </div>
          <div>
            <span>Drafts</span>
            <span>2</span>
          </div>
          <div>
            <span>Submitted</span>
            <span>7</span>
          </div>
          <div>
            <span>Published</span>
            <span>18</span>
          </div>
          <div>
            <span>Rejected</span>
            <span>2</span>
          </div>
        </div>
        <div>
          <div className="relative">
            {/* Search Icon */}
            <CiSearch className="text-xl absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 dark:text-custom-white" />

            {/* Input Field */}
            <input
              className="w-70 dark:text-custom-white border border-gray-500 dark:border-custom-white rounded-md pl-10 pr-3 py-2 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-600 dark:focus-visible:ring-white dark:focus-visible:text-white focus-visible:border-gray-600 dark:focus-visible:border-white"
              type="search"
              placeholder="Find users by name, email..."
            />
            <IoFilterOutline className="text-xl absolute right-205 top-1/2 -translate-y-1/2 text-gray-500 dark:text-custom-white" />
          </div>
        </div>
        <div>
          <table>
            <caption>A summary of the content&apos;s table</caption>
            <thead>
              <tr>
                <th scope="col">Post Title</th>
                <th scope="col">Author</th>
                <th scope="col">Date</th>
                <th scope="col">Role</th>
                <th scope="col">Status</th>
                <th scope="col">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>The Future of UI/UX: Trends...</td>
                <td>TECHIVE</td>
                <td>29/12/24</td>
                <td>Admin</td>
                <td>Published</td>
                <td>...</td>
              </tr>
              <tr>
                <td>The rise of blockchain in Re...</td>
                <td>Adeyinka Favor</td>
                <td>26/12/24</td>
                <td>Contributor</td>
                <td>Published</td>
                <td>...</td>
              </tr>
            </tbody>
          </table>
        </div>
        {/* Static Pagination */}
        <div className="max-w-7xl mx-auto mt-8 flex items-center justify-center">
          <div className="flex items-center space-x-2">
            <Button variant="outline" className="!border-gray-500">
              <MdKeyboardArrowLeft className="w-5 h-5 text-gray-500" />
            </Button>

            <span className="text-gray-600">1</span>
            <span className="text-gray-600">2</span>
            <span className="text-gray-600">...</span>
            <span className="text-gray-600">4</span>
            <Button variant="outline" className="!border-gray-500">
              <MdKeyboardArrowRight className="w-5 h-5 text-gray-500" />
            </Button>
          </div>
        </div>
      </div>

      {/* Analytics */}
      <div>
        <div>
          <div>
            <div>
              <div>
                <span>Time on page</span>
                <span>3.2 min</span>
                <p>
                  <GoArrowUpRight />
                  <span>+1.01% this week</span>
                </p>
              </div>
              <div>
                <span>Bounce rate</span>
                <span>42%</span>
                <p>
                  <GoArrowUpRight />
                  <span>+0.12% this week</span>
                </p>
              </div>
              <div>
                <span>Load speed</span>
                <span>1.0 min</span>
                <p>
                  <GoArrowDownRight />
                  <span>-1.01% this week</span>
                </p>
              </div>
            </div>
            <div>
              <div>
                <h3>Top Hashtag Performance</h3>
                <p>...</p>
              </div>
              <div>
                <h3>Crypto</h3>
                <p>1.5k Engagements</p>
              </div>
            </div>
          </div>
          <div>
            <div>
              <h3>Device types</h3>
              <form>
                <select className="dark:text-custom-white dark:bg-dark py-2 px-4 border border-gray-300 rounded-md focus-visible:outline-none focus-visible:ring-2 focus:ring-gray-700">
                  <option value="">Weekly</option>
                  <option value="monthly">Monthly</option>
                </select>
              </form>
            </div>
            <div>The graph</div>
            <div>
              <span>Mobile</span>
              <span>Tablet</span>
              <span>Desktop</span>
            </div>
          </div>
        </div>
        <div>
          <div>
            <h3>Device types</h3>
            <form>
              <select className="dark:text-custom-white dark:bg-dark py-2 px-4 border border-gray-300 rounded-md focus-visible:outline-none focus-visible:ring-2 focus:ring-gray-700">
                <option value="">Weekly</option>
                <option value="monthly">Monthly</option>
              </select>
            </form>
            <p>The graph</p>
            <div>
              <span>Registered Users</span>
              <span>Visitors</span>
              <span>Total Active Users</span>
            </div>
          </div>
          <div>
            <h3>Top Performing Post</h3>
            <form>
              <select className="dark:text-custom-white dark:bg-dark py-2 px-4 border border-gray-300 rounded-md focus-visible:outline-none focus-visible:ring-2 focus:ring-gray-700">
                <option value="">Weekly</option>
                <option value="monthly">Monthly</option>
              </select>
            </form>
            <p>The graph</p>
            <div>
              <span>Views</span>
              <span>Shares</span>
            </div>
          </div>
        </div>
      </div>

      {/* Settings */}
      <div>
        <form>
          <label htmlFor="">Site Name</label>
          <input type="text" name="" id="" value="TECHIVE" />

          <label htmlFor="">Password</label>
          <input type="text" name="" id="" value="*******" />
          <img
            className="w-5 h-5"
            src="/src/assets/icons/streamline_invisible-2.png"
            alt="An icon to toggle the visibility of password"
          />

          <label htmlFor="">Tagline</label>
          <input type="text" name="" id="" />

          <label htmlFor="">Default Language</label>
          <select className="dark:text-custom-white dark:bg-dark py-2 px-4 border border-gray-300 rounded-md focus-visible:outline-none focus-visible:ring-2 focus:ring-gray-700">
            <option value="">English</option>
            <option value="french">French</option>
          </select>

          <label htmlFor="">Color</label>
          <select className="dark:text-custom-white dark:bg-dark py-2 px-4 border border-gray-300 rounded-md focus-visible:outline-none focus-visible:ring-2 focus:ring-gray-700">
            <option value="">Pink</option>
            <option value="purple">Purple</option>
          </select>

          <label htmlFor="">Typography</label>
          <select className="dark:text-custom-white dark:bg-dark py-2 px-4 border border-gray-300 rounded-md focus-visible:outline-none focus-visible:ring-2 focus:ring-gray-700">
            <option value="">Inter</option>
            <option value="roboto">Roboto</option>
          </select>

          <div>
            <p>Enable Two-factor Authentication</p>
            <p>
              <BsToggleOn />
            </p>
          </div>

          <Button>Save Changes</Button>
        </form>
      </div>
    </div>
  );
}

export default AdminDashboard;
