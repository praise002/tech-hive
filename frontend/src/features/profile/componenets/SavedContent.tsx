import Text from '../../../components/common/Text';
import Articles from '../../../components/sections/Articles';

function SavedContent() {
  return (
    <>
      {/* <div className="md:w-xs w-60 dark:text-custom-white">
            <img
              className="w-full h-full"
              src="/assets/icons/amico.png"
              alt="An empty profile"
            />
            <div className="text-xs md:text-sm text-center mt-4">
              No saved articles yet!
            </div>
          </div> */}
      <Text
        variant="h3"
        size="lg"
        bold={false}
        className="font-semibold mb-1 md:text-2xl dark:text-custom-white lg:mt-4 px-4 lg:px-8"
      >
        Saved Articles
      </Text>

      <Articles marginTop={8} visibleHeader={false} />
    </>
  );
}

export default SavedContent;
