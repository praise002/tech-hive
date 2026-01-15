import { useParams } from 'react-router-dom';
import Rectangle from '../../components/common/Rectangle';
import SocialLinks from '../../components/common/SocialLinks';
import Text from '../../components/common/Text';
import CategoryBar from '../../components/sections/CategoryBar';
import Subscribe from '../../components/sections/Subscribe';
import { useJobDetail } from '../../hooks/useContent';
import Loader from '../../components/common/Loader';

function TechJobDetail() {
  const { id } = useParams<{ id: string }>();
  const { job, isPending, isError, error } = useJobDetail(id || '');

  if (isPending) {
    return (
      <div className="flex justify-center items-center h-screen">
        <Loader />
      </div>
    );
  }

  if (isError || !job) {
    return (
      <div className="text-center py-20 text-red-500">
        Error loading job: {error?.message}
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
            title={`${job.title} at ${job.company}`}
            sharemsg="Check out this job opportunity!"
            url={window.location.href}
          />
        </div>

        {/* Right Column: Content */}
        <div className="p-2 w-full md:w-3/4 mt-20 md:mt-10 border border-gray">
          <div>
            <Text
              variant="h3"
              size="xl"
              bold={false}
              className="font-semibold mb-2 dark:text-custom-white"
            >
              {job.title}
            </Text>
            <div className="text-secondary text-sm">{job.company}</div>
          </div>

          {/* Tags Section */}
          <div className="flex gap-2 flex-wrap my-4">
            <span className="inline-flex items-center px-2 py-1 bg-cream text-xs font-medium text-gray-700 rounded-sm">
              🌍 {job.work_mode}
            </span>
            <span className="inline-flex items-center px-2 py-1 bg-cream text-xs font-medium text-gray-700 rounded-sm">
              ⏳ {job.job_type}
            </span>
            {job.location && (
              <span className="inline-flex items-center px-2 py-1 bg-cream text-xs font-medium text-gray-700 rounded-sm">
                📍 {job.location}
              </span>
            )}
            {job.category && (
              <span className="inline-flex items-center px-2 py-1 bg-cream text-xs font-medium text-gray-700 rounded-sm">
                📂 {job.category.name}
              </span>
            )}
          </div>

          <div className="space-y-8 text-primary dark:text-custom-white">
            {/* Description */}
            <div>
              <Text
                variant="h5"
                size="lg"
                bold={false}
                className="font-semibold mb-2 dark:text-custom-white"
              >
                Job Description
              </Text>
              <div
                className="text-base md:text-lg leading-relaxed"
                dangerouslySetInnerHTML={{ __html: job.desc }}
              />
            </div>

            {/* Requirements */}
            <div>
              <Text
                variant="h5"
                size="lg"
                bold={false}
                className="font-semibold mb-2 dark:text-custom-white"
              >
                Requirements
              </Text>
              <div
                className="text-base md:text-lg leading-relaxed"
                dangerouslySetInnerHTML={{ __html: job.requirements }}
              />
            </div>

            {/* Responsibilities */}
            <div>
              <Text
                variant="h5"
                size="lg"
                bold={false}
                className="font-semibold mb-2 dark:text-custom-white"
              >
                Responsibilities
              </Text>
              <div
                className="text-base md:text-lg leading-relaxed"
                dangerouslySetInnerHTML={{ __html: job.responsibilities }}
              />
            </div>

            {/* Job Link */}
            <div>
              <Text
                variant="h5"
                size="lg"
                bold={false}
                className="font-semibold mb-2 dark:text-custom-white"
              >
                How to Apply
              </Text>
              <div className="flex gap-2 items-center text-base md:text-lg">
                <img
                  src="/assets/icons/solar_link-bold.png"
                  className="dark:invert"
                  alt=""
                />
                <a
                  href={job.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  aria-label="View Job website (opens in new tab)"
                >
                  {job.url}
                </a>
              </div>
            </div>
          </div>
          {/* <div className="text-secondary text-sm my-4">Posted 1 hour ago</div> */}
        </div>

        {/* Mobile social link */}
        <div className="block md:hidden text-center">
          <SocialLinks
            visible={false}
            title={`${job.title} at ${job.company}`}
            sharemsg="Check out this job opportunity!"
            url={window.location.href}
          />
        </div>
      </div>

      <Rectangle />
      <Subscribe />
    </>
  );
}

export default TechJobDetail;
