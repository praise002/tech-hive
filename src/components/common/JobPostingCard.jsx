import Button from './Button';
import Text from './Text';
import JobTags from './JobTags';
import PropTypes from 'prop-types';

function JobPostingCard({ job }) {
  return (
    <div className="p-6 rounded-lg border border-[#C1C8C7] shadow-lg h-full flex flex-col">
      <div className="flex-grow space-y-2">
        {/* Job Title */}
        <Text
          variant="h4"
          size="xl"
          bold={false}
          className="font-semibold text-gray-900"
        >
          {job.title}
        </Text>

        {/* Company Name */}
        <div className="text-[#889392] text-sm">{job.company}</div>

        {/* Tags Section */}
        <JobTags tags={job.tags} />
      </div>

      <div className="space-y-2">
        {/* View Details Button */}
        <Button variant="outline" className="font-medium">
          View Details
        </Button>

        {/* Posted Time */}

        <div className="text-[#889392] text-xs">
          Posted {job.lastPosted} ago
        </div>
      </div>
    </div>
  );
}

JobPostingCard.propTypes = {
  job: PropTypes.shape({
    title: PropTypes.string.isRequired,
    company: PropTypes.string.isRequired,
    lastPosted: PropTypes.string.isRequired,
    tags: PropTypes.arrayOf(PropTypes.string).isRequired,
  }).isRequired,
};

export default JobPostingCard;
