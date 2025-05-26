import { useCurrentEditor } from '@tiptap/react';

const MenuBar = () => {
  const { editor } = useCurrentEditor();

  if (!editor) {
    return null;
  }

  function ButtonClass(isActive) {
    return `p-2 rounded-lg cursor-pointer focus-visible:outline-0 focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-offset-red-300 transition duration-300 ${
      isActive ? 'bg-red text-white hover:bg-red-800' : 'bg-gray-200 text-black'
    }`;
  }

  return (
    <div className="">
      <div className="space-x-2 space-y-2">
        <button
          onClick={() => editor.chain().focus().toggleBold().run()}
          disabled={!editor.can().chain().focus().toggleBold().run()}
          className={ButtonClass(editor.isActive('bold'))}
        >
          Bold
        </button>
        <button
          onClick={() => editor.chain().focus().toggleItalic().run()}
          disabled={!editor.can().chain().focus().toggleItalic().run()}
          className={ButtonClass(editor.isActive('italic'))}
        >
          Italic
        </button>
        <button
          onClick={() => editor.chain().focus().toggleStrike().run()}
          disabled={!editor.can().chain().focus().toggleStrike().run()}
          className={ButtonClass(editor.isActive('strike'))}
        >
          Strike
        </button>
        <button
          onClick={() => editor.chain().focus().toggleCode().run()}
          disabled={!editor.can().chain().focus().toggleCode().run()}
          className={ButtonClass(editor.isActive('code'))}
        >
          Code
        </button>
        <button
          onClick={() => editor.chain().focus().unsetAllMarks().run()}
          className="bg-gray-200 text-black p-2 rounded-lg cursor-pointer focus-visible:outline-0 focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-offset-red-300 transition duration-300"
        >
          Clear marks
        </button>
        <button
          onClick={() => editor.chain().focus().clearNodes().run()}
          className="bg-gray-200 text-black p-2 rounded-lg cursor-pointer focus-visible:outline-0 focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-offset-red-300 transition duration-300"
        >
          Clear nodes
        </button>
        <button
          onClick={() => editor.chain().focus().setParagraph().run()}
          className={ButtonClass(editor.isActive('paragraph'))}
        >
          Paragraph
        </button>
        <button
          onClick={() =>
            editor.chain().focus().toggleHeading({ level: 1 }).run()
          }
          className={ButtonClass(editor.isActive('heading', { level: 1 }))}
        >
          H1
        </button>
        <button
          onClick={() =>
            editor.chain().focus().toggleHeading({ level: 2 }).run()
          }
          className={ButtonClass(editor.isActive('heading', { level: 2 }))}
        >
          H2
        </button>
        <button
          onClick={() =>
            editor.chain().focus().toggleHeading({ level: 3 }).run()
          }
          className={ButtonClass(editor.isActive('heading', { level: 3 }))}
        >
          H3
        </button>
        <button
          onClick={() =>
            editor.chain().focus().toggleHeading({ level: 4 }).run()
          }
          className={ButtonClass(editor.isActive('heading', { level: 4 }))}
        >
          H4
        </button>
        <button
          onClick={() =>
            editor.chain().focus().toggleHeading({ level: 5 }).run()
          }
          className={ButtonClass(editor.isActive('heading', { level: 5 }))}
        >
          H5
        </button>
        <button
          onClick={() =>
            editor.chain().focus().toggleHeading({ level: 6 }).run()
          }
          className={ButtonClass(editor.isActive('heading', { level: 6 }))}
        >
          H6
        </button>
        <button
          onClick={() => editor.chain().focus().toggleBulletList().run()}
          className={ButtonClass(editor.isActive('bulletList'))}
        >
          Bullet list
        </button>
        <button
          onClick={() => editor.chain().focus().toggleOrderedList().run()}
          className={ButtonClass(editor.isActive('orderedList'))}
        >
          Ordered list
        </button>
        <button
          onClick={() => editor.chain().focus().toggleCodeBlock().run()}
          className={ButtonClass(editor.isActive('codeBlock'))}
        >
          Code block
        </button>
        <button
          onClick={() => editor.chain().focus().toggleBlockquote().run()}
          className={ButtonClass(editor.isActive('blockquote'))}
        >
          Blockquote
        </button>
        <button
          onClick={() => editor.chain().focus().setHorizontalRule().run()}
          className="bg-gray-200 text-black p-2 rounded-lg cursor-pointer focus-visible:outline-0 focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-offset-red-300 transition duration-300"
        >
          Horizontal rule
        </button>
        <button
          onClick={() => editor.chain().focus().setHardBreak().run()}
          className="bg-gray-200 text-black p-2 rounded-lg cursor-pointer focus-visible:outline-0 focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-offset-red-300 transition duration-300"
        >
          Hard break
        </button>
        <button
          onClick={() => editor.chain().focus().undo().run()}
          disabled={!editor.can().chain().focus().undo().run()}
          className="bg-gray-200 text-black p-2 rounded-lg cursor-pointer focus-visible:outline-0 focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-offset-red-300 transition duration-300"
        >
          Undo
        </button>
        <button
          onClick={() => editor.chain().focus().redo().run()}
          disabled={!editor.can().chain().focus().redo().run()}
          className="bg-gray-200 text-black p-2 rounded-lg cursor-pointer focus-visible:outline-0 focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-offset-red-300 transition duration-300"
        >
          Redo
        </button>
        <button
          onClick={() => editor.chain().focus().setColor('#a32816').run()}
          className={ButtonClass(editor.isActive('textStyle', { color: '#a32816' }))}
        >
          Red
        </button>
      </div>
    </div>
  );
};

export default MenuBar;
