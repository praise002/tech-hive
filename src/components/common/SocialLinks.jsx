import Text from './Text';

function SocialLinks() {
  return (
    <div className="inline-flex flex-col p-2 space-y-4 items-center justify-center">
      <Text variant="h4" size="sm" bold={false} className="font-semibold">
        Quick AI
      </Text>
      <div>
        <img src="/src/assets/icons/AI article summary.png" alt="" />
      </div>
      <Text variant="h4" size="sm" bold={false} className="font-semibold">
        Share
      </Text>
      <div>
        <img src="/src/assets/icons/prime_twitter.png" alt="" />
      </div>
      <div>
        <img src="/src/assets/icons/uil_facebook.png" alt="" />
      </div>
      <div>
        <img src="/src/assets/icons/mdi_linkedin.png" alt="" />
      </div>
      <div>
        <img src="/src/assets/icons/mdi_instagram.png" alt="" />
      </div>
      <div>
        <img src="/src/assets/icons/fluent_share-ios-24-filled.png" alt="" />
      </div>
    </div>
  );
}

export default SocialLinks;
