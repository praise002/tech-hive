import { useParams } from 'react-router-dom';
import Image from '../../components/common/Image';
import Rectangle from '../../components/common/Rectangle';
import SocialLinks from '../../components/common/SocialLinks';
import Text from '../../components/common/Text';
import CategoryBar from '../../components/sections/CategoryBar';
import Subscribe from '../../components/sections/Subscribe';
import { useToolDetail } from '../../hooks/useContent';
import Spinner from '../../components/common/Spinner';
import Button from '../../components/common/Button';

function TechToolDetail() {
  const { toolId } = useParams<{ toolId: string }>();
  const { tool, isPending, isError, error } = useToolDetail(toolId || '');

  if (isPending) {
    return (
      <div className="flex justify-center items-center h-screen">
        <Spinner />
      </div>
    );
  }

  if (isError || !tool) {
    return (
      <div className="text-center py-20 text-red-500">
        Error loading tool: {error?.message}
      </div>
    );
  }

  return (
    <>
      <CategoryBar />
      <div className="flex flex-col md:flex-row gap-8 px-4 md:px-10 py-8">
        {/* Left Column: Social Links */}
        <div className="hidden md:block px-10 mt-70">
          <SocialLinks
            visible={false}
            title={tool.name}
            sharemsg="Check out this awesome tool!"
            url={window.location.href}
          />
        </div>

        {/* Right Column: Content */}
        <div className="w-full md:w-3/4 mt-20 md:mt-10 border border-gray rounded-tl-lg rounded-tr-lg overflow-hidden">
          {tool && (
            <Image
              alt={tool.name}
              src="/assets/tech-tool/figma.png"
              className="w-full h-64 md:h-80 object-cover shadow-md"
            />
          )}

          <div className="space-y-8 px-2 text-primary dark:invert">
            <Text
              variant="h3"
              size="xl"
              bold={false}
              className="font-semibold mt-4"
            >
              What is {tool.name}?
            </Text>

            {/* Description */}
            <div>
              <Text
                variant="h5"
                size="lg"
                bold={false}
                className="font-semibold mb-2"
              >
                Software Description
              </Text>
              <div
                className="text-base md:text-lg leading-relaxed"
                dangerouslySetInnerHTML={{ __html: tool.desc }}
              />
            </div>

            {/* How to Access */}
            <div>
              <Text
                variant="h5"
                size="lg"
                bold={false}
                className="font-semibold mb-2"
              >
                How to Access
              </Text>
              <div className="flex gap-2 items-center text-base md:text-lg">
                <img src="/assets/icons/solar_link-bold.png" alt="" />
                <a
                  href={tool.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  aria-label={`Visit ${tool.name} website (opens in new tab)`}
                >
                  {tool.url}
                </a>
              </div>
            </div>
          </div>
          <div className="px-2 text-secondary text-sm my-4 flex">
            <Button
              variant="primary"
              onClick={() => window.open(tool.url, '_blank')}
              className="w-full md:w-auto"
            >
              {tool.call_to_action || 'Explore'}
            </Button>
          </div>
        </div>

        {/* Mobile social link */}
        <div className="block md:hidden text-center">
          <SocialLinks
            visible={false}
            title={tool.name}
            sharemsg="Check out this awesome tool!"
            url={window.location.href}
          />
        </div>
      </div>

      <Rectangle />
      <Subscribe />
    </>
  );
}

export default TechToolDetail;
