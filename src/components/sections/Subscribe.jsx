import Button from '../common/Button';
import Text from '../common/Text';

function Subscribe() {
  return (
    <div>
      <div className="bg-[#ffebe4] m-6">
        <Text variant="h2" size="2xl">
          Subscribe to Our Newsletter
        </Text>
        <form action="">
          <input type="email" placeholder="Enter your email" name="" id="" />
          <Button type="submit" onClick={() => alert('Subscribed!')}>
            Subscribe
          </Button>
        </form>
      </div>
      <div></div>
    </div>
  );
}

// TODO: BUTTON CHANGES TO SUBSCRIBED

export default Subscribe;
