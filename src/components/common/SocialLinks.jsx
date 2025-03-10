import { MdOutlineSummarize } from 'react-icons/md';
import { RiShare2Line } from 'react-icons/ri';
import {
  FaXTwitter,
  FaSquareFacebook,
  FaLinkedin,
  FaInstagram,
} from 'react-icons/fa6';
import Text from './Text';
import PropTypes from 'prop-types';

function SocialLinks({ visible }) {
  return (
    <div className="dark:text-custom-white inline-flex flex-row md:flex-col p-2 gap-x-4 md:gap-y-4 items-center justify-center cursor-pointer">
      {/* Quick AI Section */}
      {visible && (
        <>
          <Text
            variant="h5"
            size="xs"
            bold={false}
            className="font-semibold dark:text-custom-white"
          >
            Quick AI
          </Text>
          <div>
            <MdOutlineSummarize
              className="w-6 h-6"
              aria-label="AI Article Summary icon"
            />
          </div>
        </>
      )}

      {/* Share Section */}
      <Text
        variant="h5"
        size="xs"
        bold={false}
        className="font-semibold dark:text-custom-white"
      >
        Share
      </Text>

      {/* Social Media Icons */}
      <div>
        <FaXTwitter className="w-6 h-6" aria-label="Twitter icon" />
      </div>
      <div>
        <FaSquareFacebook className="w-6 h-6" aria-label="Facebook icon" />
      </div>
      <div>
        <FaLinkedin className="w-6 h-6" aria-label="LinkedIn icon" />
      </div>
      <div>
        <FaInstagram className="w-6 h-6" aria-label="Instagram icon" />
      </div>
      <div>
        <RiShare2Line className="w-6 h-6" aria-label="Share Icon" />
      </div>
    </div>
  );
}

SocialLinks.propTypes = {
  visible: PropTypes.bool.isRequired,
};

export default SocialLinks;
