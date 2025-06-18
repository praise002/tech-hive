import { useCurrentEditor } from '@tiptap/react';
import { useCallback, useState } from 'react';
import toast from 'react-hot-toast';
import Spinner from '../../components/common/Spinner';

export function ButtonClass(isActive) {
  return `p-2 rounded-lg cursor-pointer focus-visible:outline-0 focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-offset-red-300 transition duration-300 ${
    isActive ? 'bg-red text-white hover:bg-red-800' : 'bg-gray-200 text-black'
  }`;
}

const MenuBar = () => {
  const { editor } = useCurrentEditor();
  const [isImageLoading, setIsImageLoading] = useState(false);

  function getImageUrl(event) {
    const file = event.target.files[0];
    if (file) {
      const imageUrl = URL.createObjectURL(file);
      console.log(imageUrl);
      return imageUrl;
    }
  }

  const addImage = useCallback(
    (event) => {
      setIsImageLoading(true);
      const url = getImageUrl(event);

      if (!url) return;

      setIsImageLoading(true);

      const img = new Image();
      img.src = url;

      img.onload = () => {
        editor.chain().focus().setImage({ src: url }).run();
        URL.revokeObjectURL(url);
        setIsImageLoading(false);
      };

      img.onerror = () => {
        toast.error('Failed to load image');
        setIsImageLoading(false);
      };
    },
    [editor]
  );

  const setLink = useCallback(() => {
    const previousUrl = editor.getAttributes('link').href;
    const url = window.prompt('URL', previousUrl);

    // cancelled
    if (url === null) {
      return;
    }

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
      toast.error(e.message);
    }
  }, [editor]);

  if (!editor) {
    return null;
  }

  function addYoutubeVideo() {
    const url = prompt('Enter YouTube URL');

    if (url) {
      editor.commands.setYoutubeVideo({
        src: url,
        width: '100%',
        height: '315',
      });
    }
  }

  return (
    <div>
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
          className="bg-gray-200 text-black p-2 rounded-lg cursor-pointer focus-visible:outline-0 focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-offset-red-300 transition duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
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
          className={ButtonClass(
            editor.isActive('textStyle', { color: '#a32816' })
          )}
        >
          Red
        </button>

        <div className="inline relative">
          <input
            type="file"
            accept="image/*"
            className="appearance-none absolute opacity-0 inset-0 cursor-pointer"
            onChange={addImage}
          />

          {isImageLoading ? (
            <button
              className={`ButtonClass(false) ${
                isImageLoading
                  ? 'cursor-not-allowed opacity-75'
                  : 'cursor-pointer'
              }`}
              disabled={isImageLoading}
            >
              <Spinner />
            </button>
          ) : (
            <button className={ButtonClass(false)}>Set image</button>
          )}
        </div>

        <button
          className={ButtonClass(false)}
          onClick={() =>
            editor
              .chain()
              .focus()
              .insertTable({ rows: 3, cols: 3, withHeaderRow: true })
              .run()
          }
        >
          Insert table
        </button>
        <button
          className={ButtonClass(false)}
          onClick={() => editor.chain().focus().addColumnBefore().run()}
        >
          Add column before
        </button>
        <button
          className={ButtonClass(false)}
          onClick={() => editor.chain().focus().addColumnAfter().run()}
        >
          Add column after
        </button>
        <button
          className={ButtonClass(false)}
          onClick={() => editor.chain().focus().deleteColumn().run()}
        >
          Delete column
        </button>
        <button
          className={ButtonClass(false)}
          onClick={() => editor.chain().focus().addRowBefore().run()}
        >
          Add row before
        </button>
        <button
          className={ButtonClass(false)}
          onClick={() => editor.chain().focus().addRowAfter().run()}
        >
          Add row after
        </button>
        <button
          className={ButtonClass(false)}
          onClick={() => editor.chain().focus().deleteRow().run()}
        >
          Delete row
        </button>
        <button
          className={ButtonClass(false)}
          onClick={() => editor.chain().focus().deleteTable().run()}
        >
          Delete table
        </button>
        <button
          className={ButtonClass(false)}
          onClick={() => editor.chain().focus().mergeCells().run()}
        >
          Merge cells
        </button>
        <button
          className={ButtonClass(false)}
          onClick={() => editor.chain().focus().splitCell().run()}
        >
          Split cell
        </button>
        <button
          className={ButtonClass(false)}
          onClick={() => editor.chain().focus().toggleHeaderColumn().run()}
        >
          Toggle header column
        </button>
        <button
          className={ButtonClass(false)}
          onClick={() => editor.chain().focus().toggleHeaderRow().run()}
        >
          Toggle header row
        </button>
        <button
          className={ButtonClass(false)}
          onClick={() => editor.chain().focus().toggleHeaderCell().run()}
        >
          Toggle header cell
        </button>
        <button
          className={ButtonClass(false)}
          onClick={() => editor.chain().focus().mergeOrSplit().run()}
        >
          Merge or split
        </button>
        <button
          className={ButtonClass(false)}
          onClick={() =>
            editor.chain().focus().setCellAttribute('colspan', 2).run()
          }
        >
          Set cell attribute
        </button>
        <button
          className={ButtonClass(false)}
          onClick={() => editor.chain().focus().fixTables().run()}
        >
          Fix tables
        </button>
        <button
          className={ButtonClass(false)}
          onClick={() => editor.chain().focus().goToNextCell().run()}
        >
          Go to next cell
        </button>
        <button
          className={ButtonClass(false)}
          onClick={() => editor.chain().focus().goToPreviousCell().run()}
        >
          Go to previous cell
        </button>
        <button
          type="button"
          className={ButtonClass(false)}
          onClick={addYoutubeVideo}
        >
          Add YouTube Video
        </button>
        <button
          onClick={setLink}
          className={ButtonClass(editor.isActive('link'))}
        >
          Set link
        </button>
        <button
          onClick={() => editor.chain().focus().unsetLink().run()}
          disabled={!editor.isActive('link')}
          className="bg-gray-200 text-black p-2 rounded-lg cursor-pointer focus-visible:outline-0 focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-offset-red-300 transition duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Unset link
        </button>
        <button
          onClick={() => editor.chain().focus().setTextAlign('left').run()}
          className={ButtonClass(editor.isActive({ textAlign: 'left' }))}
        >
          Left
        </button>
        <button
          onClick={() => editor.chain().focus().setTextAlign('center').run()}
          className={ButtonClass(editor.isActive({ textAlign: 'center' }))}
        >
          Center
        </button>
        {/* For the options, everything in common */}
      </div>
    </div>
  );
};

export default MenuBar;
