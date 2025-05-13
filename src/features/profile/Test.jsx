import { MdCancel } from 'react-icons/md';
import Button from '../../components/common/Button';
import Text from '../../components/common/Text';

// Floating cta panel
function Test() {
  return (
    <>
      <div className="mt-30 mb-10 flex flex-col text-gray-900 border dark:border-custom-white font-medium rounded-lg w-80 mx-auto">
        <div className="flex justify-between items-center border-b border-gray  px-2 pt-2 py-1">
          <Text variant="h1" size="lg" className="mb-2 dark:text-custom-white">
            AI-Generated Summary
          </Text>

          <button type="button">
            <MdCancel className="text-red w-6 h-6" />
          </button>
        </div>
        <div className="m-3">
          <p className="bg-neutral p-4 rounded-lg">
            AI-driven interfaces, immersive experiences like VR and AR,
            hyper-personalization through data and AI, accessibility for all
            users, sustainable design practices, and the rise of no-code tools
            are key trends shaping UI/UX in 2024, requiring designers to adapt
            and innovate to stay ahead in the evolving digital landscape.
          </p>
          <div className="bg-neutral mt-2 rounded-lg w-24 h-12 flex items-center justify-center gap-1">
            <p className="bg-fill rounded-full w-2 h-2"></p>
            <p className="bg-fill rounded-full w-2 h-2"></p>
            <p className="bg-fill rounded-full w-2 h-2"></p>
          </div>
        </div>
        <div className="bg-light flex flex-col justify-center items-center p-4 gap-2 rounded-b-lg">
          <Button>Regenerate Summary</Button>
          <Button variant="outline">Read Full Article</Button>
          <div></div>
        </div>
      </div>

      <div className="relative bg-custom-white py-3 px-5 w-25 mx-auto mb-4 flex flex-col rounded-md">
        <p>Edit</p>
        <p>Archive</p>
        <p>Delete</p>
        <div
          className="absolute -top-3 right-3 w-4 h-4 bg-white"
          style={{ clipPath: 'polygon(50% 0%, 0% 100%, 100% 100%)' }}
        ></div>
      </div>

      <div className="bg-red mt-2 rounded-sm w-2 h-8 flex flex-col items-center justify-center gap-1 mx-auto mb-4">
        <p className="bg-fill rounded-full w-1 h-1"></p>
        <p className="bg-fill rounded-full w-1 h-1"></p>
        <p className="bg-fill rounded-full w-1 h-1"></p>
      </div>

      <div className="bg-white  w-70 mx-auto mb-4 p-4">
        <Text variant="h1" size="lg" className="mb-2">
          Change User Role
        </Text>
        <div className="flex flex-col gap-2">
          <Button className="bg-red !text-custom-white" variant="outline">
            Contributor
          </Button>
          <Button variant="outline">Editor</Button>
          <Button variant="outline">Subscriber</Button>
          <Button variant="outline">Admin</Button>
        </div>
      </div>

      <div className="bg-white  w-70 mx-auto mb-4 p-4">
        <Text variant="h1" size="lg" className="mb-2">
          Change User Status
        </Text>
        <div className="flex flex-col gap-2">
          <Button className="bg-red !text-custom-white" variant="outline">
            Active
          </Button>

          <Button variant="outline">Suspended</Button>
        </div>
      </div>

      <div className="bg-white flex flex-col gap-2 w-70 mx-auto mb-4 p-4">
        <Button className="bg-red !text-custom-white" variant="outline">
          Edit
        </Button>

        <Button variant="outline">Suspend</Button>
        <Button variant="outline">Delete</Button>
      </div>
    </>
  );
}

export default Test;
