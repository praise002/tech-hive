import Text from '../../../components/common/Text';

function SubmittedContent() {
  return (
    <>
      {/* <p className="font-bold text-sm">No articles submitted.</p> */}
      <Text
        variant="h3"
        size="lg"
        bold={false}
        className="font-semibold mb-4 dark:text-custom-white"
      >
        Submitted Articles
      </Text>

      <div className="space-y-4">
        <div className="border border-gray-200 rounded-lg p-4 hover:border-red transition-colors">
          <div className="flex justify-between mb-2">
            <Text
              variant="h3"
              size="base"
              bold={false}
              className="font-semibold dark:text-custom-white"
            >
              Building Scalable APIs with Node.js
            </Text>
            <span className="text-nowrap flex items-center text-xs px-2 py-1 bg-light rounded-full text-secondary">
              Under Review
            </span>
          </div>

          <p className="text-secondary text-sm mb-3 line-clamp-2">
            Learn best practices for building robust and scalable REST APIs
            using Node.js, Express, and MongoDB...
          </p>

          <div className="flex  justify-between mt-3 text-xs text-secondary">
            <span>Submitted: May 11, 2025</span>
            <div className="flex gap-3">
              <span>Expected review: 2-3 days</span>
              <button className="text-red hover:text-red-600 font-medium">
                View Details
              </button>
            </div>
          </div>
        </div>

        <div className="border border-gray-200 rounded-lg p-4 hover:border-red transition-colors">
          <div className="flex justify-between mb-2">
            <Text
              variant="h3"
              size="base"
              bold={false}
              className="font-semibold dark:text-custom-white"
            >
              Introduction to Web Accessibility
            </Text>
            <span className="text-nowrap flex items-center text-xs px-2 py-1 bg-light rounded-full text-secondary">
              Pending Review
            </span>
          </div>

          <p className="text-secondary text-sm mb-3 line-clamp-2">
            Discover how to make your websites accessible to everyone by
            implementing WCAG guidelines and best practices...
          </p>

          <div className="flex justify-between mt-3 text-xs text-secondary">
            <span>Submitted: May 9, 2025</span>
            <div className="flex gap-3">
              <span>In review queue</span>
              <button className="text-red hover:text-red-600 font-medium">
                View Details
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default SubmittedContent;
