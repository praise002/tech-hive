import { homePageTechJobs } from '../../data/jobs';
import Text from '../common/Text';
import Button from '../common/Button';
import JobPostingCard from '../common/JobPostingCard';

function TechJobs() {
  return (
    <div>
      <div className="my-4">
        <Text variant="h3" size="xl" className="sm:2xl">
          Jobs in Tech
        </Text>
        <div className="w-[20px]">
          <hr className="border-b-2 border-[#a32816]" />
        </div>
      </div>
      <div className="flex flex-col gap-y-2 ">
        {homePageTechJobs.map((job, index) => (
          <JobPostingCard key={index} job={job} />
        ))}
      </div>
      <Button className='my-4'>Explore More Jobs &rarr;</Button>
    </div>
  );
}

export default TechJobs;
