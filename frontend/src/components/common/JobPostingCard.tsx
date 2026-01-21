import Button from './Button';
import Text from './Text';

import { Link } from 'react-router-dom';
import { JobPostingCardProps } from '../../types/types';
import { formatDateB } from '../../utils/utils';

function JobPostingCard({ job }: JobPostingCardProps) {
  const getJobTypeLabel = (type: string) => {
    const lower = type.toLowerCase();
    return lower.charAt(0).toUpperCase() + lower.slice(1).replace('_', '-');
  };

  const getWorkModeLabel = (mode: string) => {
    const lower = mode.toLowerCase();
    return lower.charAt(0).toUpperCase() + lower.slice(1).replace('_', ' ');
  };

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
        <div className="text-secondary text-sm mb-4">{job.company}</div>

        {/* Tags Section - Work Mode and Job Type */}
        <div className="flex gap-2 flex-wrap mb-4">
          <span className="inline-flex items-center px-2 py-1 bg-cream text-xs font-medium text-gray-700 rounded-md">
            🌍 {getWorkModeLabel(job.work_mode)}
          </span>
          <span className="inline-flex items-center px-2 py-1 bg-cream text-xs font-medium text-gray-700 rounded-md">
            🕒 {getJobTypeLabel(job.job_type)}
          </span>
        </div>
      </div>

      <div className="space-y-2 mt-4">
        {/* View Details Button */}
        <Button variant="outline" className="font-medium">
          <Link
            to={`/jobs/${job.id}`}
            aria-label={`View details for ${job.title} at ${job.company}`}
          >
            View Details
          </Link>
        </Button>

        {/* Posted Time */}
        <div className="text-secondary text-xs">
          Posted {formatDateB(job.published_at)}
        </div>
      </div>
    </article>
  );
}

export default JobPostingCard;
