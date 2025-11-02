function ProfileSkeleton() {
  return (
    <div className="mt-15" aria-label="Loading user profile">
      <div className="bg-gray-200 dark:bg-gray-700 w-full h-40 relative animate-pulse">
        <div className="absolute transform -translate-x-1/2 top-30 md:top-1/2 left-1/2 flex flex-col items-center">
          <div>
            <div className="relative">
              <div className="w-20 h-20 md:w-40 md:h-40 rounded-full bg-gray-300 dark:bg-gray-600"></div>
            </div>
          </div>

          <div className="flex flex-col justify-center items-center mt-2">
            <div className="h-6 w-40 bg-gray-300 dark:bg-gray-600 rounded mb-2"></div>
            <div className="h-4 w-32 bg-gray-300 dark:bg-gray-600 rounded"></div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto sm:px-6 lg:px-8">
        <nav
          className="flex flex-col gap-4 mt-30 md:mt-50"
          aria-label="Profile tabs"
        >
          <div className="flex place-self-center bg-gray-200 dark:bg-gray-700 gap-2 p-2 rounded-md animate-pulse">
            <div className="h-10 w-24 bg-gray-300 dark:bg-gray-600 rounded-md"></div>
            <div className="h-10 w-36 bg-gray-300 dark:bg-gray-600 rounded-md"></div>
          </div>

          <div className="py-8">
            <div className="dark:text-custom-white p-4 md:border border-gray-200 dark:border-gray-700 rounded-lg animate-pulse">
              <div className="h-40 bg-gray-300 dark:bg-gray-600 rounded-lg"></div>
            </div>
          </div>
        </nav>
      </div>
    </div>
  );
}

export default ProfileSkeleton;
