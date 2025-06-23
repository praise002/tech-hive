// import Button from '../common/Button';
import { Link } from 'react-router-dom';

import JobPostingCard from '../common/JobPostingCard';
import Text from '../common/Text';
import { displayedTechJobs } from '../../data/jobs';

function TechJobs() {
  return (
    <div className="mt-20 lg:mt-4 max-w-7xl mx-auto px-4 lg:px-8 mb-4">
      <div className="flex justify-between items-center">
        <div className="my-4">
          <Text
            variant="h3"
            size="xl"
            className="sm:2xl dark:text-custom-white"
          >
            Jobs in Tech
          </Text>
          <div className="w-[20px]">
            <hr className="border-b-2 border-red" />
          </div>
        </div>
        <div>
          <Link
            to="/jobs"
            className="cursor-pointer text-secondary hover:text-red transition-colors"
          >
            See all
          </Link>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 h-full">
        {/* <div className="flex flex-col gap-y-2"> */}
        {displayedTechJobs.map((job) => (
          <JobPostingCard key={job.id} job={job} />
        ))}
      </div>
      {/* <Button>Explore More Jobs &rarr;</Button> */}
    </div>
  );
}

export default TechJobs;
