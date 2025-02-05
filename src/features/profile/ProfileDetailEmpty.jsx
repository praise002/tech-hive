import Text from '../../components/common/Text';

function ProfileDetailEmpty() {
  return (
    <div className="mt-20">
      <div className="bg-[#FFEBE4] "></div>
      <div>
        <img src="/src/assets/icons/Avatars.png" alt="" />
        <img src="/src/assets/icons/mynaui_edit.png" alt="" />
        <div>
          <Text
            variant="h3"
            size="lg"
            bold={false}
            className="font-semibold text-gray-900 mb-2"
          >
            Elizabeth Stone
          </Text>
          <p className="text-[#889392] text-sm">Joined 27th January 2025</p>
        </div>
      </div>

      <div>
        <div>
          <div className="flex flex-col">
            <div>
              <img src="/src/assets/icons/Chat.png" alt="" />
            </div>
            <div>
              <img src="/src/assets/icons/bookmark-light.png" alt="" />
            </div>
          </div>
          <div className="flex flex-col">
            <p>0 Comments </p>
            <p>0 Saved </p>
          </div>
        </div>
        <div>
          <div>
            <img src="/src/assets/icons/amico.png" alt="" />
          </div>
          <div>No comments or saved articles yet!</div>
        </div>
      </div>
    </div>
  );
}

export default ProfileDetailEmpty;
