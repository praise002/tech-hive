import Text from '../../../components/common/Text';
import Button from '../../../components/common/Button';

import toast from 'react-hot-toast';
import ReactCrop, { centerCrop, Crop, makeAspectCrop } from 'react-image-crop';

import { useEffect, useState } from 'react';
import {
  MdArticle,
  MdCancel,
  MdLibraryBooks,
  MdSettings,
} from 'react-icons/md';

import { FaRegBookmark } from 'react-icons/fa6';
import { RiDraftFill } from 'react-icons/ri';

import SavedContent from '../componenets/SavedContent';
import DraftsContent from '../componenets/DraftsContent';
import SubmittedContent from '../componenets/SubmittedContent';
import AccountContent from '../componenets/AccountContent';
import PublishedContent from '../componenets/PublishedContent';
import { BiMessageRounded } from 'react-icons/bi';
import CommentsContent from '../componenets/CommentsContent';

const defaultProfilePicture = '/assets/icons/Avatars.png';

interface CropImageProps {
  src: string;
  aspect?: number;
  crop: Crop;
  onCropChange: (crop: Crop) => void;
}

function CropImage({ src, aspect = 1, crop, onCropChange }: CropImageProps) {
  // fun runs when the image finishes loading
  function onImageLoad(e: React.SyntheticEvent<HTMLImageElement>) {
    const { width, height } = e.currentTarget; // image elem that just finished loading
    const initialCrop = centerCrop(
      makeAspectCrop(
        {
          unit: '%',
          width: 80,
        },
        aspect,
        width,
        height
      ),
      width,
      height
    );

    onCropChange(initialCrop);
  }

  return (
    <ReactCrop
      crop={crop}
      aspect={aspect}
      onChange={(_, percentCrop) => onCropChange(percentCrop)} // Notify parent when crop changes
    >
      <img src={src ?? undefined} alt="Preview" onLoad={onImageLoad} />
    </ReactCrop>
  );
}

function AccountDetail() {
  const [isActiveTab, setIsActiveTab] = useState('saved');
  const [isEditingPc, setIsEditingPc] = useState(false);
  const [isEditingName, setIsEditingName] = useState(false);

  const [showCropModal, setShowCropModal] = useState(false);

  const [tempImage, setTempImage] = useState<string | null>(null);

  const [profile, setProfile] = useState({
    name: 'Elizabeth Stone',
    profilePicture: defaultProfilePicture,
  });

  const [crop, setCrop] = useState<Crop>({
    x: 0,
    y: 0,
    width: 80,
    height: 80,
    unit: '%',
  });

  async function handleSetProfilePicture() {
    if (!tempImage) return;
    if (!crop) return;

    try {
      // Step 1: Load the image into a canvas
      const image = new Image();
      image.src = tempImage;

      await new Promise((resolve) => {
        image.onload = resolve;
      });

      // Step 2: Apply the crop
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');

      // Calculate pixel values from percentages (if crop is in %)
      const scaleX = image.naturalWidth / image.width;
      const scaleY = image.naturalHeight / image.height;

      const pixelCrop = {
        x:
          crop.unit === '%'
            ? (crop.x / 100) * image.naturalWidth
            : crop.x * scaleX,
        y:
          crop.unit === '%'
            ? (crop.y / 100) * image.naturalHeight
            : crop.y * scaleY,
        width:
          crop.unit === '%'
            ? (crop.width / 100) * image.naturalWidth
            : crop.width * scaleX,
        height:
          crop.unit === '%'
            ? (crop.height / 100) * image.naturalHeight
            : crop.height * scaleY,
      };

      canvas.width = pixelCrop.width;
      canvas.height = pixelCrop.height;

      ctx?.drawImage(
        image, // What to draw
        pixelCrop.x, // Where to start cutting (horizontal)
        pixelCrop.y, // Where to start cutting (vertical)
        pixelCrop.width, // How wide to cut
        pixelCrop.height, // How tall to cut
        0, // Where to place on canvas (horizontal)
        0, // Where to place on canvas (vertical)
        pixelCrop.width, // How wide to make it on canvas
        pixelCrop.height // How tall to make it on canvas
      );

      // Step 3: Convert canvas to blob and update profile
      canvas.toBlob((blob) => {
        if (!blob) return;
        const croppedImageUrl = URL.createObjectURL(blob);
        setProfile((prev) => ({
          ...prev,
          profilePicture: croppedImageUrl,
        }));
        setShowCropModal(false);
        setTempImage(null);
        toast.success('Profile picture updated successfully!');
      });
    } catch (error) {
      console.error('Error cropping image:', error);
      toast.error('Failed to crop image');
    }
  }

  useEffect(() => {
    type DropdownEvent = MouseEvent | KeyboardEvent;

    function handleCloseDropdown(event: DropdownEvent): void {
      // Handle escape key
      if (
        event.type === 'keydown' &&
        event instanceof KeyboardEvent &&
        event.key === 'Escape'
      ) {
        setIsEditingPc(false);
        return;
      }

      // Handle click outside
      if (event.type === 'mousedown') {
        const dropdown = document.getElementById('edit-pc-links-dropdown');

        if (dropdown && !dropdown.contains(event.target as Node)) {
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
    function handleCloseModal(event: Event) {
      // Handle escape key
      if (
        event.type === 'keydown' &&
        event instanceof KeyboardEvent &&
        event.key === 'Escape'
      ) {
        setShowCropModal(false);
        return;
      }

      // Handle click outside
      if (event.type === 'mousedown') {
        const modalContent = document.querySelector('.crop-modal-content');
        if (modalContent && !modalContent.contains(event.target as Node)) {
          setShowCropModal(false);
        }
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

  function handleProfilePicChange(event: React.ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (file) {
      const imageUrl = URL.createObjectURL(file);
      // Store the image temporarily and show modal
      setTempImage(imageUrl);
      setShowCropModal(true);
    }

    setIsEditingPc(false); // close dropdown
  }

  // function handleSetProfilePicture() {
  //   // Apply cropped image to profile
  //   if (tempImage) {
  //     setProfile((prev) => ({
  //       ...prev,
  //       profilePicture: tempImage,
  //     }));
  //     setShowCropModal(false);
  //     setTempImage(null);
  //     toast.success('Profile picture updated successfully!');
  //   }
  // }

  function handleCloseCropModal() {
    // Cancel the upload and clean up
    setShowCropModal(false);
    if (tempImage) {
      URL.revokeObjectURL(tempImage); // Cleanup memory
      setTempImage(null);
    }
  }

  const profileTabs = [
    {
      id: 'comments',
      label: 'Comments',
      icon: <BiMessageRounded className="w-5 h-5" />,
      comments: [6, 10, 15],
    },
    {
      id: 'saved',
      label: 'Saved',
      icon: <FaRegBookmark className="w-5 h-5" />,
    },
    {
      id: 'drafts',
      label: 'Drafts',
      icon: <RiDraftFill className="w-5 h-5" />,
    },
    {
      id: 'submitted',
      label: 'Submitted',
      icon: <MdArticle className="w-5 h-5" />,
    },
    {
      id: 'published',
      label: 'Published Articles',
      icon: <MdLibraryBooks className="w-5 h-5" />,
      published: [1005, 1006],
    },
    {
      id: 'account',
      label: 'Account',
      icon: <MdSettings className="w-5 h-5" />,
    },
  ];

  function getContent() {
    switch (isActiveTab) {
      case 'comments':
        return <CommentsContent />;
      case 'saved':
        return <SavedContent />;
      case 'drafts':
        return <DraftsContent />;
      case 'submitted':
        return <SubmittedContent />;
      case 'account':
        return <AccountContent />;
      case 'published':
        return <PublishedContent />;
      default:
        return <CommentsContent />;
    }
  }

  return (
    <div className="mt-15">
      {/* ✅ Profile Header */}
      <div className="bg-light w-full h-40 relative">
        {/* ✅ SVG Background */}
        <img
          src="/assets/hero-section.svg"
          alt="Background"
          className="pointer-events-none absolute inset-0 w-full h-full object-cover opacity-70"
        />
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
                aria-label="Edit profile picture"
              >
                {/* Edit icon that stays fixed */}
                <img
                  className="w-5 h-5 md:w-7 md:h-7 pointer-events-none" // Prevents clicks on the icon itself
                  src="/assets/icons/mynaui_edit.png"
                  alt=""
                />
              </button>

              {isEditingPc && (
                <div
                  id="edit-pc-links-dropdown"
                  className="p-2 absolute left-15 top-20 sm:left-45 sm:top-35 bg-light w-40 flex flex-col rounded-md"
                  role="menu"
                  aria-label="Profile picture actions"
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
              className="crop-modal-content bg-white mt-30 mb-10 flex flex-col gap-2 text-gray-900 text-xs sm:text-sm border dark:border-custom-white font-medium rounded-lg max-w-80 sm:max-w-100 max-h-[80vh]"
              onClick={(e) => e.stopPropagation()} // Prevent closing when clicking inside
            >
              <div className="flex items-center justify-between gap-2 border-b border-gray px-2 pt-2 py-1">
                <Text variant="h1" size="lg" className="mb-2">
                  Crop your new profile picture
                </Text>
                <button
                  type="button"
                  onClick={handleCloseCropModal}
                  aria-label="Close profile modal"
                >
                  <MdCancel className="text-red w-6 h-6" aria-hidden="true" />
                </button>
              </div>
              <div className="overflow-y-scroll p-2 flex justify-center">
                {tempImage && (
                  <CropImage
                    src={tempImage}
                    crop={crop}
                    onCropChange={setCrop}
                  />
                )}
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

      <div className="flex flex-col px-10 md:px-20 md:mt-10 mt-15">
        <div className="max-w-7xl mx-auto sm:px-6 lg:px-8">
          <nav
            className="flex flex-col gap-4 mt-30 md:mt-50"
            aria-label="Profile tabs"
          >
            <div className="flex place-self-center bg-light gap-2 p-2 rounded-md">
              {profileTabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setIsActiveTab(tab.id)}
                  className={`flex p-2 items-center gap-2 rounded-md text-xs sm:text-base cursor-pointer ${
                    isActiveTab === tab.id && 'bg-red text-custom-white'
                  }`}
                  aria-label={`View ${tab.label}`}
                  aria-pressed={isActiveTab === tab.id}
                >
                  <span className="flex-shrink-0">{tab.icon}</span>
                  <span
                    className={`${
                      isActiveTab == tab.id ? 'inline' : 'hidden md:inline'
                    }`}
                  >
                    {tab.label}
                  </span>
                </button>
              ))}
            </div>

            <div className="py-8">
              <div className="dark:text-custom-white w-full">
                {getContent()}
              </div>
            </div>
          </nav>
        </div>
      </div>
    </div>
  );
}

export default AccountDetail;
