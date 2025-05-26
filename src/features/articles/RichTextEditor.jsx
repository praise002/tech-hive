import {
  useEditor,
  FloatingMenu,
  BubbleMenu,
  EditorProvider,
} from '@tiptap/react';
import StarterKit from '@tiptap/starter-kit';

import Button from '../../components/common/Button';
import Text from '../../components/common/Text';

import Placeholder from '@tiptap/extension-placeholder';
import MenuBar from './MenuBar';
import TextStyle from '@tiptap/extension-text-style';
import ListItem from '@tiptap/extension-list-item';

// define your extension array
const extensions = [
  TextStyle.configure({ types: [ListItem.name] }),
  StarterKit.configure({
    heading: {
      levels: [1, 2, 3, 4, 5, 6],
    },
    bulletList: {
      keepMarks: true,
      keepAttributes: false, // TODO : Making this as `false` becase marks are not preserved when I try to preserve attrs, awaiting a bit of help
    },
    orderedList: {
      keepMarks: true,
      keepAttributes: false, // TODO : Making this as `false` becase marks are not preserved when I try to preserve attrs, awaiting a bit of help
    },
  }),
  Placeholder.configure({
    placeholder: 'Start writing your article...',
  }),
];
const content = '';

function RichTextEditor() {
  const editor = useEditor({
    extensions,
    content,
    placeholder: 'Start writing your article...',
  });
  // Show contributor's Dashboard depending on who logged in using auth later
  return (
    <div className="py-20 px-4 sm:px-6 lg:px-8">
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

      <div className="p-2 border border-gray-800 dark:border-custom-white rounded-md">
        <EditorProvider
          slotBefore={<MenuBar />}
          extensions={extensions}
          content={content}
          editorProps={{
            attributes: {
              class: 'focus:outline-none min-h-[300px]',
            },
          }}
        ></EditorProvider>
      </div>

      {/* <FloatingMenu editor={editor}>+</FloatingMenu>
      <BubbleMenu editor={editor}>+</BubbleMenu> */}

      <div className="flex gap-2 mt-5">
        <Button variant="outline">Save as Draft</Button>
        <Button>Publish</Button>
      </div>
    </div>
  );
}
// for admin and contributor, change the title based on the role
export default RichTextEditor;
