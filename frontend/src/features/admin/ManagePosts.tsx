import { CiSearch } from "react-icons/ci";
import { GoPlus } from "react-icons/go";
import { IoFilterOutline } from "react-icons/io5";
import Articles from "../../components/sections/Articles";
import TechJobs from "../../components/sections/TechJobs";
import TechEvents from "../../components/sections/TechEvents";
import TechTool from "../../components/sections/TechTool";
import ResourceSpotlight from "../../components/sections/ResourceSpotlight";

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

export default ManagePosts;