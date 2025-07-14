import { MdCancel, MdOutlineSummarize } from 'react-icons/md';
import { RiShare2Line } from 'react-icons/ri';
import { FaXTwitter, FaSquareFacebook, FaLinkedin } from 'react-icons/fa6';
import {
  FaWhatsapp,
  FaTelegram,
  FaEnvelope,
  FaReddit,
  FaLink,
} from 'react-icons/fa';

import { useEffect, useState } from 'react';
import toast from 'react-hot-toast';
import Button from './Button';
import Text from './Text';
import { SocialLinksProps, ToolTipProps } from '../../types/types';

export function ToolTip({ children, text, position = 'top' }: ToolTipProps) {
  const positionClasses: Record<string, string> = {
    top: 'top-7 left-1/2 -translate-x-1/2 md:-translate-0 md:-top-0 md:left-8',
    bottom: 'top-full right-1/2 -translate-x-1/2 mt-2',
    // left: 'right-full top-1/2 -translate-y-1/2 mr-2',
    // right: 'left-full top-1/2 -translate-y-1/2 ml-2',
  };
  return (
    <div className="relative group">
      {children}
      <div
        className={`opacity-0 group-hover:opacity-100 transition-opacity absolute px-2 py-1 bg-black text-custom-white text-xs rounded whitespace-nowrap ${positionClasses[position]}`}
      >
        {text}
      </div>
    </div>
  );
}

// Helper function to generate share URLs
function getShareUrl(
  platform: string,
  url: string,
  title: string,
  sharemsg: string,
  content: string
) {
  const message = encodeURIComponent(`${title} ${url}`);
  // const shareMessage = `Check out this article on ${title}`;
  const shareMessage = `${sharemsg} ${title}`;
  const body = `${content.slice(0, 20)}.\n\nRead more: ${url}`;

  switch (platform) {
    case 'twitter':
      return `https://twitter.com/intent/tweet?text=${message}`;
    case 'facebook':
      return `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(
        url
      )}`;
    case 'linkedin':
      return `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(
        url
      )}`;
    case 'whatsapp':
      return `https://wa.me/?text=${message}`;
    case 'telegram':
      return `https://t.me/share/url?url=${encodeURIComponent(
        url
      )}&text=${encodeURIComponent(shareMessage)}`;
    case 'reddit':
      return `https://www.reddit.com/submit?url=${encodeURIComponent(
        url
      )}&title=${encodeURIComponent(title)}`;
    case 'email':
      return `mailto:?subject=${encodeURIComponent(
        shareMessage
      )}&body=${encodeURIComponent(body)}`;
    default:
      return '#';
  }
}

function SocialLinks({
  visible,
  title,
  sharemsg,
  url,
  content = '',
}: SocialLinksProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [isSummarizeModal, setIsSummarizeModal] = useState(false);

  // const summary =
  //   'This article explores the future of UI/UX design, focusing on trends like AI-powered interfaces, immersive experiences, and personalized user interactions. Designers must adapt to these emerging technologies to stay ahead.';

  // TODO: FIX LATER: SO MANY WAYS OF DOING IT
  // Function to handle clicks outside the dropdown
  useEffect(() => {
    interface MouseEvent {
      target: EventTarget | null;
    }

    function handleClickOutside(event: MouseEvent): void {
      const dropdown = document.getElementById('social-links-dropdown');

      if (dropdown && !dropdown.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen]);

  useEffect(() => {
    function handleEscapeKey(event: KeyboardEvent): void {
      if (event.key === 'Escape') {
        closeSummarizeModal();
        setIsOpen(false);
      }
    }

    if (isSummarizeModal || isOpen) {
      document.addEventListener('keydown', handleEscapeKey);
    }

    return () => {
      document.removeEventListener('keydown', handleEscapeKey);
    };
  }, [isSummarizeModal, isOpen]);

  function handleToggleShare() {
    setIsOpen((prev) => !prev);
  }

  // Summarize handler
  function openSummarizeModal() {
    setIsSummarizeModal(true);
  }

  function closeSummarizeModal() {
    setIsSummarizeModal(false);
  }

  const primaryIcons = [
    {
      id: 'Twitter',
      icon: <FaXTwitter className="w-6 h-6" aria-label="Twitter icon" />,
      platform: 'twitter',
    },
    {
      id: 'Facebook',
      icon: <FaSquareFacebook className="w-6 h-6" aria-label="Facebook icon" />,
      platform: 'facebook',
    },
    {
      id: 'Linkedin',
      icon: (
        <FaLinkedin key="" className="w-6 h-6" aria-label="LinkedIn icon" />
      ),
      platform: 'linkedin',
    },
    {
      id: 'Share',
      icon: (
        <RiShare2Line key="share" className="w-6 h-6" aria-label="Share Icon" />
      ),
      onClick: handleToggleShare,
    },
  ];

  const secondaryIcons = [
    {
      id: 'WhatsApp',
      icon: <FaWhatsapp className="w-6 h-6" aria-label="WhatsApp icon" />,
      platform: 'whatsapp',
    },
    {
      id: 'Telegram',
      icon: <FaTelegram className="w-6 h-6" aria-label="Telegram icon" />,
      platform: 'telegram',
    },
    {
      id: 'Email',
      icon: <FaEnvelope className="w-6 h-6" aria-label="Email icon" />,
      platform: 'email',
    },
    {
      id: 'Reddit',
      icon: <FaReddit className="w-6 h-6" aria-label="Reddit icon" />,
      platform: 'reddit',
    },
  ];

  // Generic share handler
  function handleShare(platform: string) {
    const shareUrl = getShareUrl(platform, url, title, sharemsg, content);
    window.open(shareUrl, '_blank');
    setIsOpen(false); // Close the dropdown after sharing
  }

  // Copy link handler
  function handleCopyLink() {
    navigator.clipboard
      .writeText(url)
      .then(() => {
        toast.success('Link copied to clipboard!');
      })
      .catch(() => toast.error('Failed to copy the link.'));
  }

  return (
    <div className="relative dark:text-custom-white inline-flex flex-row md:flex-col p-2 gap-x-4 md:gap-y-4 items-center justify-center cursor-pointer">
      {/* Quick AI Section */}

      {visible && (
        <ToolTip text="AI Summarize">
          <button type="button" onClick={openSummarizeModal}>
            <MdOutlineSummarize
              className="w-6 h-6"
              aria-label="AI Article Summary icon"
            />
          </button>
        </ToolTip>
      )}

      {/* Modal Overlay */}
      {isSummarizeModal && (
        <div
          className="fixed inset-0 flex items-center justify-center bg-black z-50"
          onClick={closeSummarizeModal} // Close modal when clicking outside
          role="dialog"
          aria-modal="true"
          aria-labelledby="modal-title"
        >
          {/* Modal Content */}
          <div
            className="bg-white mt-30 mb-10 flex flex-col text-gray-900 text-xs sm:text-sm border dark:border-custom-white font-medium rounded-lg max-w-80"
            onClick={(e) => e.stopPropagation()} // Prevent closing when clicking inside
          >
            <div className="flex justify-between items-center border-b border-gray px-2 pt-2 py-1">
              <Text variant="h1" size="lg" className="mb-2">
                AI-Generated Summary
              </Text>

              <button
                type="button"
                onClick={closeSummarizeModal}
                aria-label="Close summary modal"
              >
                <MdCancel className="text-red w-6 h-6" />
              </button>
            </div>
            <div className="m-3">
              <p className="bg-neutral p-4 rounded-lg">
                AI-driven interfaces, immersive experiences like VR and AR,
                hyper-personalization through data and AI, accessibility for all
                users, sustainable design practices, and the rise of no-code
                tools are key trends shaping UI/UX in 2024, requiring designers
                to adapt and innovate to stay ahead in the evolving digital
                landscape.
              </p>
              <div className="bg-neutral mt-2 rounded-lg w-24 h-12 flex items-center justify-center gap-1">
                <p className="bg-fill rounded-full w-2 h-2"></p>
                <p className="bg-fill rounded-full w-2 h-2"></p>
                <p className="bg-fill rounded-full w-2 h-2"></p>
              </div>
            </div>
            <div className="bg-light flex flex-col justify-center items-center p-4 gap-2 rounded-b-lg">
              <Button>Regenerate Summary</Button>
              <Button variant="outline" onClick={closeSummarizeModal}>
                Read Full Article
              </Button>
              <div></div>
            </div>
          </div>
        </div>
      )}

      {/* Primary Social Media Icons */}
      {primaryIcons.map((icon) => (
        <ToolTip key={icon.id} text={icon.id}>
          <button
            onClick={() => {
              icon.onClick ? icon.onClick() : handleShare(icon.platform);
            }}
          >
            {icon.icon}
          </button>
        </ToolTip>
      ))}

      {/* Secondary Social Icons (Dropdown) */}
      {isOpen && (
        <div
          id="social-links-dropdown"
          className="absolute -bottom-62 left-1/2 sm:-bottom-55 sm:left-50 md:left-12 md:-bottom-55 space-y-2 flex flex-col justify-center shadow-2xl rounded-md p-2 border bg-white dark:bg-black border-primary dark:border-secondary"
        >
          {secondaryIcons.map((icon) => (
            <button
              key={icon.id}
              className="flex items-center gap-4 p-2 hover:bg-red hover:text-custom-white transition-colors"
              onClick={() => handleShare(icon.platform)}
            >
              <div>{icon.icon}</div>
              <div className="text-nowrap ">Share to {icon.id}</div>
            </button>
          ))}
          <button
            onClick={handleCopyLink}
            className="flex items-center gap-4 p-2 hover:bg-red hover:text-custom-white transition-colors"
          >
            <div>
              <FaLink className="w-6 h-6" />
            </div>
            <div className="text-nowrap ">Copy link</div>
          </button>
        </div>
      )}
    </div>
  );
}

export default SocialLinks;
