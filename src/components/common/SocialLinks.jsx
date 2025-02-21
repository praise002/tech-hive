import Text from './Text';
import PropTypes from 'prop-types';

function SocialLinks({ visible }) {
  return (
    <div className="dark:invert inline-flex flex-row md:flex-col p-2 gap-x-4 md:gap-y-4 items-center justify-center cursor-pointer">
      {/* Quick AI Section */}
      {visible && (
        <>
          <Text variant="h5" size="xs" bold={false} className="font-semibold dark:text-custom-white">
            Quick AI
          </Text>
          <div className="w-6 h-6">
            <img
              src="/src/assets/icons/AI article summary.png"
              alt="AI Article Summary"
              className="w-full h-full" 
            />
          </div>
        </>
      )}

      {/* Share Section */}
      <Text variant="h5" size="xs" bold={false} className="font-semibold">
        Share
      </Text>

      {/* Social Media Icons */}
      <div className="w-6 h-6" >
        <img
          src="/src/assets/icons/prime_twitter.png"
          alt="Twitter"
          className="w-full h-full" 
        />
      </div>
      <div className="w-6 h-6" >
        <img
          src="/src/assets/icons/uil_facebook.png"
          alt="Facebook"
          className="w-full h-full" 
        />
      </div>
      <div className="w-6 h-6" >
        <img
          src="/src/assets/icons/mdi_linkedin.png"
          alt="LinkedIn"
          className="w-full h-full" 
        />
      </div>
      <div className="w-6 h-6" >
        <img
          src="/src/assets/icons/mdi_instagram.png"
          alt="Instagram"
          className="w-full h-full" 
        />
      </div>
      <div className='w-6 h-6'>
        <img
          src="/src/assets/icons/fluent_share-ios-24-filled.png"
          alt="Share Icon"
          className="w-full h-full" 
        />
      </div>
    </div>
  );
}

SocialLinks.propTypes = {
  visible: PropTypes.bool.isRequired,
};

export default SocialLinks;