import Text from '../../../components/common/Text';

function CommentsContent() {
  return (
    // <p className="font-bold text-sm">No recent comments available.</p>
    <>
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
        <p className="text-secondary text-sm mb-1">Africa Fintech Summit</p>
      </div>
      <div className="flex items-center gap-2 text-xs md:text-sm">
        <p className="font-bold">Thanks for the info</p>
        <p className="text-secondary">27th January, 2025</p>
      </div>
    </>
  );
}

export default CommentsContent;
