import Text from '../../components/common/Text';
import Button from '../../components/common/Button';
import ArticleCard from '../../components/common/ArticleCard';
import SubscriptionStatus from '../subscription/SubscriptionStatus';
import toast from 'react-hot-toast';
import ReactCrop from 'react-image-crop';
import PropTypes from 'prop-types';
import { useEffect, useState } from 'react';
import { MdCancel } from 'react-icons/md';

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

const defaultProfilePicture = '/src/assets/icons/Avatars.png';

function CropImage({ src }) {
  // Starting with a preselected crop
  const [crop, setCrop] = useState({
    unit: '%', // Can be 'px' or '%'
    x: 25,
    y: 25,
    width: 50,
    height: 50,
  });
  return (
    <ReactCrop crop={crop} onChange={(c) => setCrop(c)}>
      <img src={src} alt="Preview" />
    </ReactCrop>
  );
}

CropImage.propTypes = {
  src: PropTypes.string.isRequired,
};

function AccountDetail() {
  const [isEditingPc, setIsEditingPc] = useState(false);
  const [isEditingName, setIsEditingName] = useState(false);
  // controls when the modal appears
  const [showCropModal, setShowCropModal] = useState(false);
  // Stores the uploaded image temporarily
  const [tempImage, setTempImage] = useState(null);

  const [profile, setProfile] = useState({
    name: 'Elizabeth Stone',
    profilePicture: defaultProfilePicture,
  });

  // TODO: FIX LATER: SO MANY WAYS OF DOING IT
  useEffect(() => {
    function handleCloseDropdown(event) {
      // Handle escape key
      if (event.type === 'keydown' && event.key === 'Escape') {
        setIsEditingPc(false);
        return;
      }

      // Handle click outside
      if (event.type === 'mousedown') {
        const dropdown = document.getElementById('edit-pc-links-dropdown');

        if (dropdown && !dropdown.contains(event.target)) {
          setIsEditingPc(false);
        }
      }
    }

    if (isEditingPc) {
      document.addEventListener('mousedown', handleCloseDropdown);
      document.addEventListener('keydown', handleCloseDropdown);
    }

    return () => {
      document.removeEventListener('mousedown', handleCloseDropdown);
      document.removeEventListener('keydown', handleCloseDropdown);
    };
  }, [isEditingPc]);

  useEffect(() => {
    function handleCloseModal(event) {
      // Handle escape key
      if (event.type === 'keydown' && event.key === 'Escape') {
        setShowCropModal(false);
        return;
      }

      // Handle click outside
      if (event.type === 'mousedown') {
        setShowCropModal(false);
      }
    }

    if (showCropModal) {
      document.addEventListener('mousedown', handleCloseModal);
      document.addEventListener('keydown', handleCloseModal);
    }

    return () => {
      document.removeEventListener('mousedown', handleCloseModal);
      document.removeEventListener('keydown', handleCloseModal);
    };
  }, [showCropModal]);

  function handleProfilePicChange(event) {
    const file = event.target.files[0];
    if (file) {
      const imageUrl = URL.createObjectURL(file);
      // Store the image temporarily and show modal
      setTempImage(imageUrl);
      setShowCropModal(true);
    }

    setIsEditingPc(false); // close dropdown
  }

  function handleSetProfilePicture() {
    // Apply cropped image to profile
    if (tempImage) {
      setProfile((prev) => ({
        ...prev,
        profilePicture: tempImage,
      }));
      setShowCropModal(false);
      setTempImage(null);
      toast.success('Profile picture updated successfully!');
    }
  }

  function handleCloseCropModal() {
    // Cancel the upload and clean up
    setShowCropModal(false);
    if (tempImage) {
      URL.revokeObjectURL(tempImage); // Cleanup memory
      setTempImage(null);
    }
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
              <button
                onClick={() => setIsEditingPc(true)}
                className="absolute top-12 right-0 md:top-25 bg-light rounded-full p-1 md:p-2 cursor-pointer focus-visible:outline-0 focus-visible:ring-2 focus-visible:ring-red transition duration-300"
              >
                {/* Edit icon that stays fixed */}
                <img
                  className="w-5 h-5 md:w-7 md:h-7 pointer-events-none" // Prevents clicks on the icon itself
                  src="/src/assets/icons/mynaui_edit.png"
                  alt="Edit"
                />
              </button>

              {isEditingPc && (
                <div
                  id="edit-pc-links-dropdown"
                  className="p-2 absolute left-45 top-35 bg-light w-40 flex flex-col rounded-md"
                >
                  <div className="relative cursor-pointer duration-300 hover:bg-red-800 hover:text-white">
                    {/* Hidden file input for profile picture upload */}
                    <input
                      type="file"
                      accept="image/*"
                      className="appearance-none absolute inset-0 opacity-0  w-full h-full"
                      onChange={handleProfilePicChange}
                    />
                    <button
                      type="button"
                      className="p-1 focus-visible:outline-0 focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-offset-red-300 transition duration-300"
                    >
                      Upload a photo
                    </button>
                  </div>

                  <div>
                    <button
                      type="button"
                      onClick={() => {
                        setIsEditingPc(false);
                        setProfile((prev) => ({
                          ...prev,
                          profilePicture: defaultProfilePicture,
                        }));
                      }}
                      className="p-1 cursor-pointer focus-visible:outline-0 focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-offset-red-300 transition duration-300 hover:bg-red-800 hover:text-white"
                    >
                      Remove a photo
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>

          <div className="flex flex-col justify-center items-center">
            {isEditingName ? (
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
            {!isEditingName && (
              <Button variant="outline" onClick={() => setIsEditingName(true)}>
                Edit Profile
              </Button>
            )}
            {isEditingName && (
              <div className="flex space-x-2 mt-2">
                <Button
                  variant="gradient"
                  onClick={() => {
                    toast.success('Profile updated successfully!');
                    setIsEditingName(false);
                  }}
                >
                  Save
                </Button>
                <Button
                  variant="outline"
                  onClick={() => setIsEditingName(false)}
                >
                  Cancel
                </Button>
              </div>
            )}
          </div>
        </div>

        {showCropModal && (
          /* Modal Overlay */
          <div
            className="fixed inset-0 flex items-center justify-center backdrop-contrast-50 z-50"
            role="dialog"
            aria-modal="true"
            aria-labelledby="modal-title"
          >
            {/* Modal Content */}
            <div
              className="bg-white mt-30 mb-10 flex flex-col gap-2 text-gray-900 text-xs sm:text-sm border dark:border-custom-white font-medium rounded-lg max-w-100"
              onClick={(e) => e.stopPropagation()} // Prevent closing when clicking inside
            >
              <div className="flex items-center gap-2 border-b border-gray px-2 pt-2 py-1">
                <Text variant="h1" size="lg" className="mb-2">
                  Crop your new profile picture
                </Text>
                <button
                  type="button"
                  onClick={handleCloseCropModal}
                  aria-label="Close profile modal"
                >
                  <MdCancel className="text-red w-6 h-6" />
                </button>
              </div>
              <div className="overflow-y-scroll p-2 flex justify-center">
                <CropImage src={tempImage} />
              </div>
              <div className="p-2">
                <Button className="w-full" onClick={handleSetProfilePicture}>
                  Set new profile picture
                </Button>
              </div>
            </div>
          </div>
        )}
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
