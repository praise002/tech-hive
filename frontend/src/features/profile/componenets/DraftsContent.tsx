import Text from '../../../components/common/Text';

function DraftsContent() {
  return (
    <>
      {/* <div className="md:w-xs w-60 dark:text-custom-white">
            <img
              className="w-full h-full"
              src="/assets/icons/amico.png"
              alt="An empty profile"
            />
            <div className="text-xs md:text-sm text-center mt-4">
              No drafts available.
            </div>
          </div> */}
      <Text
        variant="h3"
        size="lg"
        bold={false}
        className="font-semibold mb-4 dark:text-custom-white"
      >
        My Drafts
      </Text>

      <div className="space-y-4">
        <div className="border border-gray-200 rounded-lg p-4 hover:border-red transition-colors">
          <div className="flex justify-between items-start mb-2">
            <Text
              variant="h3"
              size="base"
              bold={false}
              className="font-semibold dark:text-custom-white"
            >
              Getting Started with React Hooks
            </Text>
            <span className="text-nowrap text-xs px-2 py-1 bg-light rounded-full text-secondary">
              In Progress
            </span>
          </div>

          <p className="text-secondary text-sm mb-3 line-clamp-2">
            React Hooks are a powerful feature that allows you to use state and
            other React features without writing a class component...
          </p>

          <div className="flex items-center gap-4">
            <div className="flex-1 h-2 bg-gray-200 rounded-full">
              <div
                className="h-full bg-red rounded-full"
                style={{ width: '75%' }}
              />
            </div>
            <span className="text-xs text-secondary">75% complete</span>
          </div>

          <div className="flex items-center justify-between mt-3 text-xs text-secondary">
            <span>Last edited: May 10, 2025</span>
            <button className="text-red hover:text-red-600 font-medium">
              Continue Editing
            </button>
          </div>
        </div>

        <div className="border border-gray-200 rounded-lg p-4 hover:border-red transition-colors">
          <div className="flex justify-between items-start mb-2">
            <Text
              variant="h3"
              size="base"
              bold={false}
              className="font-semibold dark:text-custom-white"
            >
              Understanding TypeScript Generics
            </Text>
            <span className="text-nowrap text-xs px-2 py-1 bg-light rounded-full text-secondary">
              Just Started
            </span>
          </div>

          <p className="text-secondary text-sm mb-3 line-clamp-2">
            TypeScript generics provide a way to make components work with any
            data type while maintaining type safety...
          </p>

          <div className="flex items-center gap-4">
            <div className="flex-1 h-2 bg-gray-200 rounded-full">
              <div
                className="h-full bg-red rounded-full"
                style={{ width: '30%' }}
              />
            </div>
            <span className="text-xs text-secondary">30% complete</span>
          </div>

          <div className="flex items-center justify-between mt-3 text-xs text-secondary">
            <span>Last edited: May 8, 2025</span>
            <button className="text-red hover:text-red-600 font-medium">
              Continue Editing
            </button>
          </div>
        </div>
      </div>
    </>
  );
}

export default DraftsContent;
