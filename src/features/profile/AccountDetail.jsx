import Text from '../../components/common/Text';
import Button from '../../components/common/Button';
import ArticleCard from '../../components/common/ArticleCard';
import { useState } from 'react';
import SubscriptionStatus from '../subscription/SubscriptionStatus';
import toast from 'react-hot-toast';

const article = {
  image: '/src/assets/articles/the-future-ui-ux.jpg',
  title: 'The Power of Data: How Analytics is Driving Business Decisions',
  description:
    'Learn how data analytics is transforming industries and helping businesses make smarter, data-driven decisions...',
  tags: ['Data Analytics', 'Business', 'Technology'],
  reactions: ['❤️', '😍', '👍', '🔥'],
  reactionsCount: 105,
  posted: '1 week ago',
  readTime: '7 min',
};

function AccountDetail() {
  const [isEditing, setIsEditing] = useState(false);

  const [profile, setProfile] = useState({
    name: 'Elizabeth Stone',
    profilePicture: '/src/assets/icons/Avatars.png',
  });

  function handleProfilePicChange(event) {
    const file = event.target.files[0];
    if (file) {
      const imageUrl = URL.createObjectURL(file);
      setProfile((prev) => ({
        ...prev,
        profilePicture: imageUrl,
      }));
    }

    toast.success('Profile picture updated successfully!');
  }

  function handleEditClick() {
    setIsEditing(true);
  }

  function handleSaveClick() {
    toast.success('Profile updated successfully!');
    setIsEditing(false);
  }

  function handleCancelClick() {
    setIsEditing(false);
  }

  return (
    <div className="mt-15">
      {/* ✅ Profile Header */}
      <div className="bg-light w-full h-40 relative">
        <div className="absolute transform -translate-x-1/2 top-30 md:top-1/2 left-1/2 flex flex-col items-center">
          <div>
            <div className="relative">
              <img
                className="w-20 h-20 md:w-40 md:h-40 rounded-full object-cover"
                src={profile.profilePicture}
                alt="Profile Picture"
              />

              {/* Wrapper for the edit functionality */}
              <div className="absolute top-12 right-0 md:top-25 bg-light rounded-full p-1 md:p-2">
                {/* Hidden file input for profile picture upload */}
                <input
                  type="file"
                  accept="image/*"
                  className="appearance-none absolute inset-0 opacity-0 cursor-pointer w-full h-full"
                  onChange={handleProfilePicChange}
                />
                {/* Edit icon that stays fixed */}
                <img
                  className="w-5 h-5 md:w-7 md:h-7 pointer-events-none" // Prevents clicks on the icon itself
                  src="/src/assets/icons/mynaui_edit.png"
                  alt="Edit"
                />
              </div>
            </div>
          </div>

          <div className="flex flex-col justify-center items-center">
            {isEditing ? (
              <input
                type="text"
                className="appearance-none dark:text-custom-white mt-1 px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-800 focus:border-gray-800"
                value={profile.name}
                onChange={(e) =>
                  setProfile({ ...profile, name: e.target.value })
                }
              />
            ) : (
              <Text
                variant="h3"
                size="lg"
                bold={false}
                className="font-semibold text-gray-900 dark:text-custom-white"
              >
                {profile.name}
              </Text>
            )}
            <p className="text-secondary text-sm my-1">
              Joined 27th January 2025
            </p>
            {!isEditing && (
              <Button variant="outline" onClick={handleEditClick}>
                Edit Profile
              </Button>
            )}
            {isEditing && (
              <div className="flex space-x-2 mt-2">
                <Button variant="gradient" onClick={handleSaveClick}>
                  Save
                </Button>
                <Button variant="outline" onClick={handleCancelClick}>
                  Cancel
                </Button>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* ✅ Account Information */}
      <div className="dark:text-custom-white mt-45 md:mt-50 mb-5 px-20 text-gray-900">
        <Text
          variant="h3"
          size="lg"
          bold={false}
          className="font-semibold mb-2 dark:text-custom-white"
        >
          Account Settings
        </Text>
        <div className="space-y-4">
          <div className="border border-gray rounded-lg p-4">
            <p className="font-semibold mb-1">Change Password</p>
            <Button
              variant="outline"
              onClick={() => alert('Redirecting to Change Password')}
            >
              Update Password
            </Button>
          </div>
        </div>
      </div>

      {/* ✅ Subscription Status */}
      <SubscriptionStatus />

      {/* ✅ Recent Comments & Saved Articles */}
      <div className="text-gray-900 dark:text-custom-white flex-col items-center md:items-start md:flex-row flex gap-4 mb-8 px-20">
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
    </div>
  );
}

export default AccountDetail;
