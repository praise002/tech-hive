import Button from './Button';
import Text from './Text';
import JobTags from './JobTags';

import { Link } from 'react-router-dom';
import { JobPostingCardProps } from '../../types/types';

function JobPostingCard({ job }: JobPostingCardProps) {
  return (
    <article className="p-6 rounded-lg border border-gray dark:border-gray-700 shadow-lg h-full flex flex-col">
      <div className="flex-grow space-y-2">
        {/* Job Title */}
        <Text
          variant="h4"
          size="xl"
          bold={false}
          className="font-semibold text-gray-900 dark:text-custom-white"
        >
          {job.title}
        </Text>

        {/* Company Name */}
        <div className="text-secondary text-sm">{job.company}</div>

        {/* Tags Section */}
        <JobTags tags={job.tags} />
      </div>

      <div className="space-y-2">
        {/* View Details Button */}
        <Button variant="outline" className="font-medium">
          <Link to="/jobs/a" aria-label={`View details for ${job.title} at ${job.company}`}>View Details</Link>
        </Button>

        {/* Posted Time */}

        <div className="text-secondary text-xs">
          Posted {job.lastPosted} ago
        </div>
      </div>
    </article>
  );
}

export default JobPostingCard;
