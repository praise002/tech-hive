import {
  useEditor,
  FloatingMenu,
  BubbleMenu,
  EditorProvider,
} from '@tiptap/react';
import StarterKit from '@tiptap/starter-kit';

import Button from '../../components/common/Button';
import Text from '../../components/common/Text';

import MenuBar from './MenuBar';
import TextStyle from '@tiptap/extension-text-style';
import ListItem from '@tiptap/extension-list-item';
import CodeBlockLowlight from '@tiptap/extension-code-block-lowlight';
import { common, createLowlight } from 'lowlight';
import Color from '@tiptap/extension-color';
import Image from '@tiptap/extension-image';
import Table from '@tiptap/extension-table';
import TableRow from '@tiptap/extension-table-row';
import TableHeader from '@tiptap/extension-table-header';
import TableCell from '@tiptap/extension-table-cell';

// create a lowlight instance with all languages loaded or use common
const lowlight = createLowlight(common);

const extensions = [
  TextStyle.configure({ types: [ListItem.name] }),
  Color,
  Image,
  Table.configure({
    resizable: true,
  }),
  TableRow,
  TableHeader,
  TableCell,
  StarterKit.configure({
    // Disable the default CodeBlock extension
    codeBlock: false,
  }),
  CodeBlockLowlight.configure({
    lowlight,
    defaultLanguage: 'javascript',
  }),
];

let content = `<pre><code class="language-javascript">const foo = "bar"</code></pre>
      <pre><code class="language-css">body { color: red }</code></pre>
      <pre><code class="language-python">name = "bar"</code></pre>
      <img src="https://placehold.co/800x400" />
      <table>
          <tbody>
            <tr>
              <th>Name</th>
              <th colspan="3">Description</th>
            </tr>
            <tr>
              <td>Cyndi Lauper</td>
              <td>Singer</td>
              <td>Songwriter</td>
              <td>Actress</td>
            </tr>
          </tbody>
        </table>`;

content = '';

function RichTextEditor() {
  const editor = useEditor({
    extensions,
    content,
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

      <div className="w-full p-2 border border-gray-800 dark:border-custom-white rounded-md">
        <EditorProvider
          slotBefore={<MenuBar />}
          extensions={extensions}
          content={content}
          editorProps={{
            attributes: {
              class:
                'w-full max-w-none list-decimal focus:outline-none min-h-[300px] prose dark:prose-invert',
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

// NOTE: Tell user to press triple enter to exit code block
// TODO: FIX CODE LIGHTER, FIX UNDO NOT DISABLING
// use react syntax highlighter
// create a custom component to replace the default code block renderer
// just like the one shown in syntax highlighter docs
// Finish reading the tiptap docs
// Placeholder issue
// Style list-disc: can't use default one
