import Button from '../common/Button';
import JobPosting from '../common/JobPosting';
import Text from '../common/Text';

function TechJobs() {
  return (
    <div>
      <div className="my-4">
        <Text
          variant="h3"
          size="xl"
          bold={false}
          className="font-semibold sm:2xl"
        >
          Jobs in Tech
        </Text>
        <div className="w-[20px]">
          <hr className="border-b-2 border-[#a32816]" />
        </div>
      </div>

      <JobPosting />
      <Button>Explore More Jobs &rarr;</Button>
    </div>
  );
}

export default TechJobs;
