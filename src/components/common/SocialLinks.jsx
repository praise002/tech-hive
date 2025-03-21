import { MdOutlineSummarize } from 'react-icons/md';
import { RiShare2Line } from 'react-icons/ri';
import { FaXTwitter, FaSquareFacebook, FaLinkedin } from 'react-icons/fa6';
import {
  FaWhatsapp,
  FaTelegram,
  FaEnvelope,
  FaReddit,
  FaLink,
} from 'react-icons/fa';
import PropTypes from 'prop-types';
import { useEffect, useState } from 'react';
import toast from 'react-hot-toast';

// close if outside is being clicked

// Helper function to generate share URLs
function getShareUrl(platform, url, title, content) {
  const message = encodeURIComponent(`${title} ${url}`);
  const shareMessage = `Check out this article on ${title}`;
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

function SocialLinks({ visible, title, url, content = '' }) {
  const [isOpen, setIsOpen] = useState(false);
  // const summary =
  //   'This article explores the future of UI/UX design, focusing on trends like AI-powered interfaces, immersive experiences, and personalized user interactions. Designers must adapt to these emerging technologies to stay ahead.';

  // Function to handle clicks outside the dropdown
  useEffect(() => {
    function handleClickOutside(event) {
      const dropdown = document.getElementById('social-links-dropdown');

      if (dropdown && !dropdown.contains(event.target)) {
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

  function handleToggleShare() {
    setIsOpen((prev) => !prev);
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
  function handleShare(platform) {
    const shareUrl = getShareUrl(platform, url, title, content);
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

  function ToolTip({ children, text }) {
    return (
      <div className="relative group">
        {children}
        <div className="opacity-0 group-hover:opacity-100 transition-opacity absolute -top-0 left-8  px-2 py-1 bg-black text-custom-white text-xs rounded whitespace-nowrap">
          {text}
        </div>
      </div>
    );
  }

  ToolTip.propTypes = {
    children: PropTypes.node.isRequired,
    text: PropTypes.string.isRequired,
  };

  return (
    <div className="relative dark:text-custom-white inline-flex flex-row md:flex-col p-2 gap-x-4 md:gap-y-4 items-center justify-center cursor-pointer">
      {/* Quick AI Section */}

      {visible && (
        <ToolTip text="AI Summarize">
          <MdOutlineSummarize
            className="w-6 h-6"
            aria-label="AI Article Summary icon"
          />
        </ToolTip>
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

SocialLinks.propTypes = {
  visible: PropTypes.bool.isRequired,

  title: PropTypes.string.isRequired,
  content: PropTypes.string,
  url: PropTypes.string.isRequired,
};

export default SocialLinks;
