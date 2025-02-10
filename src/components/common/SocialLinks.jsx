import Text from './Text';
import PropTypes from 'prop-types';

function SocialLinks({ visible }) {
  return (
    <div className="inline-flex flex-row md:flex-col p-2 space-x-4 md:space-y-4 items-center justify-center cursor-pointer">
      {/* Quick AI Section */}
      {visible && (
        <>
          <Text variant="h5" size="xs" bold={false} className="font-semibold">
            Quick AI
          </Text>
          <div>
            <img
              src="/src/assets/icons/AI article summary.png"
              alt="AI Article Summary"
              className="w-8 h-8" 
            />
          </div>
        </>
      )}

      {/* Share Section */}
      <Text variant="h5" size="xs" bold={false} className="font-semibold">
        Share
      </Text>

      {/* Social Media Icons */}
      <div>
        <img
          src="/src/assets/icons/prime_twitter.png"
          alt="Twitter"
          className="w-6 h-6" 
        />
      </div>
      <div>
        <img
          src="/src/assets/icons/uil_facebook.png"
          alt="Facebook"
          className="w-6 h-6" 
        />
      </div>
      <div>
        <img
          src="/src/assets/icons/mdi_linkedin.png"
          alt="LinkedIn"
          className="w-6 h-6" 
        />
      </div>
      <div>
        <img
          src="/src/assets/icons/mdi_instagram.png"
          alt="Instagram"
          className="w-6 h-6" 
        />
      </div>
      <div className='mr-4'>
        <img
          src="/src/assets/icons/fluent_share-ios-24-filled.png"
          alt="Share Icon"
          className="w-6 h-6" 
        />
      </div>
    </div>
  );
}

SocialLinks.propTypes = {
  visible: PropTypes.bool.isRequired,
};

export default SocialLinks;