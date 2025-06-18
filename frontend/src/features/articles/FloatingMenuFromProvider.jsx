import { FloatingMenu, useCurrentEditor } from '@tiptap/react';

import { FaBold, FaItalic } from 'react-icons/fa6';
import { MdFormatListBulleted } from 'react-icons/md';
import { GrBlockQuote } from 'react-icons/gr';

export function FloatingMenuFromProvider() {
  const { editor } = useCurrentEditor();

  if (!editor) return null;

  return (
    <FloatingMenu editor={editor} tippyOptions={{ duration: 100 }}>
      <div className="bg-white rounded-xl shadow-lg flex p-2 space-x-3">
        <button
          onClick={() =>
            editor.chain().focus().toggleHeading({ level: 1 }).run()
          }
          className={`p-2 rounded-lg cursor-pointer focus-visible:outline-0 focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-offset-red-300 transition duration-300 ${
            editor.isActive('heading', { level: 1 })
              ? 'bg-red text-white'
              : 'hover:bg-gray-200'
          }`}
        >
          H1
        </button>
        <button
          onClick={() =>
            editor.chain().focus().toggleHeading({ level: 2 }).run()
          }
          className={`p-2 rounded-lg cursor-pointer focus-visible:outline-0 focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-offset-red-300 transition duration-300 ${
            editor.isActive('heading', { level: 2 })
              ? 'bg-red text-white'
              : 'hover:bg-gray-200'
          }`}
        >
          H2
        </button>
        <button
          onClick={() => editor.chain().focus().toggleBold().run()}
          disabled={!editor.can().chain().focus().toggleBold().run()}
          className={`p-2 rounded-lg cursor-pointer focus-visible:outline-0 focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-offset-red-300 transition duration-300 ${
            editor.isActive('bold') ? 'bg-red text-white' : 'hover:bg-gray-200'
          }`}
        >
          <FaBold size={16} />
        </button>
        <button
          onClick={() => editor.chain().focus().toggleItalic().run()}
          disabled={!editor.can().chain().focus().toggleItalic().run()}
          className={`p-2 rounded-lg cursor-pointer focus-visible:outline-0 focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-offset-red-300 transition duration-300 ${
            editor.isActive('italic')
              ? 'bg-red text-white'
              : 'hover:bg-gray-200'
          }`}
        >
          <FaItalic size={16} />
        </button>

        <button
          onClick={() => editor.chain().focus().toggleBlockquote().run()}
          className={`p-2 rounded-lg cursor-pointer focus-visible:outline-0 focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-offset-red-300 transition duration-300 ${
            editor.isActive('blockquote')
              ? 'bg-red text-white'
              : 'hover:bg-gray-200'
          }`}
        >
          <GrBlockQuote size={16} />
        </button>

        <button
          onClick={() => editor.chain().focus().toggleBulletList().run()}
          className={`p-2 rounded-lg cursor-pointer focus-visible:outline-0 focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-offset-red-300 transition duration-300 ${
            editor.isActive('bulletList')
              ? 'bg-red text-white'
              : 'hover:bg-gray-200'
          }`}
        >
          <MdFormatListBulleted size={16} />
        </button>
      </div>
    </FloatingMenu>
  );
}

export default FloatingMenuFromProvider;
