import { BubbleMenu, useCurrentEditor } from '@tiptap/react';
import { useCallback } from 'react';
import toast from 'react-hot-toast';
import { FaBold, FaItalic, FaLink } from 'react-icons/fa6';
import { GrBlockQuote } from "react-icons/gr";

export function BubbleMenuFromProvider() {
  const { editor } = useCurrentEditor();

  if (!editor) return;

  const setLink = useCallback(() => {
    const previousUrl = editor.getAttributes('link').href;
    const url = window.prompt('URL', previousUrl);

    // cancelled
    if (url === null) return;

    // empty
    if (url === '') {
      editor.chain().focus().extendMarkRange('link').unsetLink().run();

      return;
    }

    // update link
    try {
      editor
        .chain()
        .focus()
        .extendMarkRange('link')
        .setLink({ href: url })
        .run();
    } catch (e) {
      const error = e as Error;
      toast.error(error.message);
    }
  }, [editor]);

  if (!editor) return null;

  return (
    <BubbleMenu editor={editor} tippyOptions={{ duration: 100 }}>
      <div className="bg-white rounded-xl shadow-lg flex p-2 space-x-3">
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
          onClick={setLink}
          className={`p-2 rounded-lg cursor-pointer focus-visible:outline-0 focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-offset-red-300 transition duration-300 ${
            editor.isActive('link') ? 'bg-red text-white' : 'hover:bg-gray-200'
          }`}
        >
          <FaLink size={16} />
        </button>
      </div>
    </BubbleMenu>
  );
}

export default BubbleMenuFromProvider;
