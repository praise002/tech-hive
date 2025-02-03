import Button from "../common/Button";
import Resource from "../common/Resource";
import Text from "../common/Text";

function ResourceSpotlight() {
  return (
    <div>
      <div className="my-4">
        <Text
          variant="h3"
          size="xl"
          bold={false}
          className="font-semibold sm:2xl"
        >
          Resource Spotlight
        </Text>
        <div className="w-[20px]">
          <hr className="border-b-2 border-[#a32816]" />
        </div>
      </div>
      <Resource />
      <Button>Explore More Resources &rarr;</Button>
    </div>
  );
}

export default ResourceSpotlight;
