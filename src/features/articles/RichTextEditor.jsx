import {
  useEditor,
  EditorContent,
  FloatingMenu,
  BubbleMenu,
} from '@tiptap/react';
import StarterKit from '@tiptap/starter-kit';

import Button from '../../components/common/Button';
import Text from '../../components/common/Text';

// define your extension array
const extensions = [StarterKit];
const content = '<p>Hello World!</p>';

function RichTextEditor() {
  const editor = useEditor({
    extensions,
    content,
  });
  // Show contributor's Dashboard depending on who logged in using auth later
  return (
    <div className="py-20  px-4 sm:px-6 lg:px-8">
      <Text
        variant="h1"
        size="lg"
        bold={false}
        className="font-semibold mb-1 text-gray-900 dark:text-custom-white"
      >
        Techive&apos;s Dashboard
      </Text>
      <div className="flex items-center gap-2 my-4 dark:text-custom-white">
        <button className="text-secondary focus-visible:outline-0 focus-visible:ring-2 transition duration-300">
          Edit
        </button>
        <div className="h-4 w-[1px] bg-red"></div>
        <button className="font-semibold focus-visible:outline-0 focus-visible:ring-2 transition duration-300">
          Preview
        </button>
      </div>
      {/* <div>Others</div> */}

      <EditorContent editor={editor} />
      <FloatingMenu editor={editor}>This is the floating menu</FloatingMenu>
      <BubbleMenu editor={editor}>This is the bubble menu</BubbleMenu>

      <div className="flex gap-2">
        <Button variant="outline">Save as Draft</Button>
        <Button>Publish</Button>
      </div>
    </div>
  );
}
// for admin and contributor, change the title basedon the role
export default RichTextEditor;
