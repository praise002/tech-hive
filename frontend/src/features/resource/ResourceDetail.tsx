import { useParams } from 'react-router-dom';
import Image from '../../components/common/Image';
import Rectangle from '../../components/common/Rectangle';
import SocialLinks from '../../components/common/SocialLinks';
import Text from '../../components/common/Text';
import CategoryBar from '../../components/sections/CategoryBar';
import Subscribe from '../../components/sections/Subscribe';
import { useResourceDetail } from '../../hooks/useContent';
import Loader from '../../components/common/Loader';

function ResourceDetail() {
  const { id } = useParams<{ id: string }>();
  const { resource, isPending, isError, error } = useResourceDetail(id || '');

  if (isPending) {
    return (
      <div className="flex justify-center items-center h-screen">
        <Loader />
      </div>
    );
  }

  if (isError || !resource) {
    return (
      <div className="text-center py-20 text-red-500">
        Error loading resource: {error?.message}
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
            title={resource.name}
            sharemsg="Check out this resource!"
            url={window.location.href}
          />
        </div>

        {/* Right Column: Content */}
        <div className="w-full md:w-3/4 mt-20 md:mt-10 border border-gray rounded-tl-lg rounded-tr-lg overflow-hidden">
          {resource.image && (
            <Image
              alt={resource.name}
              src={resource.image}
              className="w-full h-auto shadow-md"
            />
          )}

          <div className="space-y-8 px-2 text-primary">
            <Text
              variant="h3"
              size="xl"
              bold={false}
              className="font-semibold mt-4 dark:text-custom-white"
            >
              {resource.name}
            </Text>

            {/* Description */}
            <div>
              <Text
                variant="h5"
                size="lg"
                bold={false}
                className="font-semibold mb-2 dark:text-custom-white"
              >
                Resource Description
              </Text>
              <div
                className="text-base md:text-lg leading-relaxed dark:text-custom-white"
                dangerouslySetInnerHTML={{ __html: resource.body }}
              />
            </div>

            {/* Dynamic content rendering skipped as resource model is simple: name, body, url, tags */}
            {/* If there are specific fields like 'popular_courses', they need to be in the model. Assuming generic body for now */}

            {/* Link */}
            <div>
              <Text
                variant="h5"
                size="lg"
                bold={false}
                className="font-semibold mb-2 dark:text-custom-white"
              >
                Access Resource
              </Text>
              <div className="flex gap-2 items-center text-base md:text-lg dark:text-custom-white">
                <img
                  className="dark:invert"
                  src="/assets/icons/solar_link-bold.png"
                  alt=""
                />
                <a
                  href={resource.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  aria-label={`Visit ${resource.name} (opens in new tab)`}
                >
                  {resource.url}
                </a>
              </div>
            </div>
          </div>
          {/* <div className="px-2 text-secondary text-sm my-4">
            Posted 1 hour ago
          </div> */}
        </div>

        {/* Mobile social link */}
        <div className="block md:hidden text-center">
          <SocialLinks
            visible={false}
            title={resource.name}
            sharemsg="Check out this resource!"
            url={window.location.href}
          />
        </div>
      </div>
      <Rectangle />
      <Subscribe />
    </>
  );
}

export default ResourceDetail;
