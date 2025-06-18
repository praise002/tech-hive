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

      