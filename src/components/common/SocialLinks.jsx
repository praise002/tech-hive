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
import { useState } from 'react';
import toast from 'react-hot-toast';

// close if outside is being clicked



function SocialLinks({ visible, title, url, content = '' }) {
  const [isOpen, setIsOpen] = useState(false);
  const message = encodeURIComponent(`${title} ${url}`);
  const icons = [
    {
      id: 'Twitter',
      icon: <FaXTwitter className="w-6 h-6" aria-label="Twitter icon" />,
      onClick: handleTwitterShare,
    },
    {
      id: 'Facebook',
      icon: <FaSquareFacebook className="w-6 h-6" aria-label="Facebook icon" />,
      onClick: handleFacebookShare,
    },
    {
      id: 'Linkedin',
      icon: (
        <FaLinkedin key="" className="w-6 h-6" aria-label="LinkedIn icon" />
      ),
      onClick: handleLinkedInShare,
    },
    {
      id: 'Share',
      icon: (
        <RiShare2Line key="share" className="w-6 h-6" aria-label="Share Icon" />
      ),
      onClick: handleGeneralShare,
    },
  ];

  const socialIcons = [
    {
      id: 'WhatsApp',
      icon: <FaWhatsapp className="w-6 h-6" aria-label="WhatsApp icon" />,
      onClick: handleWhatsAppShare,
    },
    {
      id: 'Telegram',
      icon: <FaTelegram className="w-6 h-6" aria-label="Telegram icon" />,
      onClick: handleTelegramShare,
    },
    {
      id: 'Email',
      icon: <FaEnvelope className="w-6 h-6" aria-label="Email icon" />,
      onClick: handleEmailShare,
    },
    {
      id: 'Reddit',
      icon: <FaReddit className="w-6 h-6" aria-label="Reddit icon" />,
      onClick: handleRedditShare,
    },
  ];

  function handleTwitterShare() {
    window.open(`https://twitter.com/intent/tweet?text=${message}`, '_blank');
  }

  function handleFacebookShare() {
    window.open(
      `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`,
      '_blank'
    );
  }

  function handleLinkedInShare() {
    window.open(
      `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(
        url
      )}`,
      '_blank'
    );
  }

  function handleWhatsAppShare() {
    window.open(`https://wa.me/?text=${message}`, '_blank');
  }

  function handleTelegramShare() {
    const shareMessage = `Check out this article on ${title}`;
    window.open(
      `https://t.me/share/url?url=${encodeURIComponent(
        url
      )}&text=${encodeURIComponent(shareMessage)}`,
      '_blank'
    );
  }

  function handleRedditShare() {
    window.open(
      `https://www.reddit.com/submit?url=${encodeURIComponent(
        url
      )}&title=${encodeURIComponent(title)}`,
      '_blank'
    );
  }

  function handleEmailShare() {
    const subject = `Check out this article on ${title}`;
    const body = `${content.slice(0, 20)}.\n\nRead more: ${url}`;
    window.open(
      `mailto:?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(
        body
      )}`,
      '_blank'
    );
  } // TODO: Yet to test

  function handleCopyLink() {
    navigator.clipboard
      .writeText(url)
      .then(() => {
        toast.success('Link copied to clipboard!');
      })
      .catch(() => toast.error('Failed to copy the link.'));
  }

  function handleGeneralShare() {
    setIsOpen((open) => !open);
  }

  return (
    <div className="relative dark:text-custom-white inline-flex flex-row md:flex-col p-2 gap-x-4 md:gap-y-4 items-center justify-center cursor-pointer">
      {/* Quick AI Section */}

      {visible && (
        <>
          <div className="relative group">
            <MdOutlineSummarize
              className="w-6 h-6"
              aria-label="AI Article Summary icon"
            />
            <div className="opacity-0 group-hover:opacity-100 absolute -top-0 left-8  px-2 py-1 bg-black text-custom-white text-xs rounded whitespace-nowrap">
              AI Summarize
            </div>
          </div>
        </>
      )}

      {/* Social Media Icons */}
      {icons.map((icon) => (
        <button className="relative group" key={icon.id} onClick={icon.onClick}>
          {icon.icon}
          <div className="opacity-0 group-hover:opacity-100 transition-opacity absolute -top-0 left-8  px-2 py-1 bg-black text-custom-white text-xs rounded whitespace-nowrap">
            {icon.id}
          </div>
        </button>
      ))}

      {isOpen && (
        <div className="absolute lg:left-12 lg:-bottom-55 space-y-2 flex flex-col justify-center shadow-2xl rounded-md p-2 border bg-white dark:bg-black border-primary dark:border-secondary">
          {socialIcons.map((icon) => (
            <button
              key={icon.id}
              className="flex items-center gap-4 p-2 hover:bg-red hover:text-custom-white transition-colors"
              onClick={icon.onClick}
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
  text: PropTypes.string.isRequired,
  title: PropTypes.string.isRequired,
  content: PropTypes.string.isRequired,
  url: PropTypes.string.isRequired,
};

export default SocialLinks;
