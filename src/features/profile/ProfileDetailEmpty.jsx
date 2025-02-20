import Text from '../../components/common/Text';

function ProfileDetailEmpty() {
  return (
    <div className="mt-15">
      <div className="bg-light w-full h-40 relative">
        <div className="absolute transform -translate-x-1/2 top-30 md:top-1/2 left-1/2 flex flex-col items-center">
          <div>
            <div className="relative">
              <img
                className="w-20 h-20 md:w-40 md:h-40"
                src="/src/assets/icons/Avatars.png"
                alt=""
              />
            </div>
            <div className="absolute top-1/3 right-10 md:right-1 md:top-1/2 bg-light rounded-full p-1 md:p-2">
              <img
                className="w-5 h-5 md:w-7 md:h-7"
                src="/src/assets/icons/mynaui_edit.png"
                alt=""
              />
            </div>
          </div>

          <div className="flex flex-col justify-center items-center">
            <Text
              variant="h3"
              size="lg"
              bold={false}
              className="font-semibold text-gray-900 mb-1"
            >
              Elizabeth Stone
            </Text>
            <p className="text-color-text-secondary text-sm">
              Joined 27th January 2025
            </p>
          </div>
        </div>
      </div>

      <div className="mt-30 md:mt-50 flex-col items-center md:items-start md:flex-row flex gap-4 mb-8 px-20">
        <div className="p-3 md:w-fit md:h-fit border border-gray rounded-lg">
          <div className="flex gap-2 items-center mb-2">
            <div className="w-4 h-4">
              <img
                className="w-full h-full"
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
                className="w-full h-full"
                src="/src/assets/icons/bookmark-light.png"
                alt=""
              />
            </div>
            <p className="font-semibold text-xs sm:text-sm md:text-lg">
              0 Saved{' '}
            </p>
          </div>
        </div>
        <div className="flex-1 p-4 border flex justify-center items-center border-gray rounded-lg">
          <div className="md:w-xs w-60">
            <img
              className="w-full h-full"
              src="/src/assets/icons/amico.png"
              alt=""
            />
            <div className="text-xs md:text-sm text-center">
              No comments or saved articles yet!
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ProfileDetailEmpty;
