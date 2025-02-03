import Image from '../common/Image';
import Tags from '../common/Tags';
import Text from '../common/Text';
import Button from '../common/Button';

function Tool() {
  return (
    <div className="relative overflow-hidden rounded-lg shadow-lg">
      <Image alt="Figma" src="/src/assets/tech-tool/figma.png" />

      <div className="p-5 border-l border-r border-b border-[#C1C8C7] rounded-bl-lg rounded-br-lg overflow-hidden">
        <Text variant="h4" size="xl" bold={false} className="font-semibold">
          Figma
        </Text>
        <div>
          A cloud-based design tool for creating, prototyping, and collaborating
          on user interfaces.
        </div>
        <Tags />
        <Button variant="outline">Try Figma for Free</Button>
      </div>
    </div>
  );
}

export default Tool;
