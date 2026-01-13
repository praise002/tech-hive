import { Toolbar } from '@liveblocks/react-tiptap';
import { Icon } from '@liveblocks/react-ui';
import { Editor } from '@tiptap/react';
import { useCallback, useState } from 'react';
import toast from 'react-hot-toast';

import {
  FaColumns,
  FaPlus,
  FaMinus,
  FaTrash,
  FaArrowLeft,
  FaArrowRight,
  FaObjectUngroup,
  FaObjectGroup,
  FaWrench,
  FaExpandArrowsAlt,
  FaUnlink,
} from 'react-icons/fa';
import {
  FaAlignCenter,
  FaAlignLeft,
  FaCode,
  FaHeading,
  FaImage,
  FaLink,
  FaTable,
  FaYoutube,
} from 'react-icons/fa6';
import Spinner from '../../../../components/common/Spinner';

function CustomToolbar({ editor }: { editor: Editor | null }) {
  if (!editor) return null;

  const [isImageLoading, setIsImageLoading] = useState(false);

  function getImageUrl(
    event: React.ChangeEvent<HTMLInputElement>
  ): string | null {
    const file = event.target.files?.[0];

    return file ? URL.createObjectURL(file) : null;
  }

  const addImage = useCallback(
    (event: React.ChangeEvent<HTMLInputElement>) => {
      setIsImageLoading(true);
      const url = getImageUrl(event);

      if (!url) return;

      setIsImageLoading(true);

      const img = new Image();

      img.src = url;

      img.onload = () => {
        editor?.chain().focus().setImage({ src: url, alt: '' }).run();
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
    if (!editor) return;

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
      toast.error((e as Error).message);
    }
  }, [editor]);

  function addYoutubeVideo() {
    const url = prompt('Enter YouTube URL');
    if (!editor) return null;

    if (url) {
      editor.commands.setYoutubeVideo({
        src: url,
        width: 640,
        // width: '100%';
        height: 315,
      });
    }
  }

  return (
    <Toolbar
      editor={editor}
      after={
        <>
          {/* TEXT FORMATTING */}
          <Toolbar.Toggle
            name="Center"
            icon={<FaAlignCenter />}
            active={editor.isActive('textAlign', { align: 'center' })}
            onClick={() => editor.chain().focus().setTextAlign('center').run()}
          />
          <Toolbar.Toggle
            name="Left"
            icon={<FaAlignLeft />}
            active={editor.isActive('textAlign', { align: 'left' })}
            onClick={() => editor.chain().focus().setTextAlign('left').run()}
          />
          {/* LINKS */}
          <Toolbar.Button name="Set link" icon={<FaLink />} onClick={setLink} />
          <Toolbar.Button
            name="Unset link"
            icon={<FaUnlink />}
            onClick={() => editor.chain().focus().unsetLink().run()}
          />
          {/* MEDIA */}
          <>
            <Toolbar.Button
              name="Add Image"
              icon={isImageLoading ? <Spinner /> : <FaImage />}
              onClick={() => document.getElementById('file-upload')?.click()}
              disabled={isImageLoading}
            />

            <input
              id="file-upload"
              type="file"
              accept="image/*"
              className="hidden"
              onChange={addImage}
            />
          </>
          <Toolbar.Button
            name="Add YouTube Video"
            icon={<FaYoutube />}
            onClick={addYoutubeVideo}
          />
          {/* CODE BLOCKS */}
          <Toolbar.Toggle
            name="Code block"
            icon={<FaCode />}
            active={editor.isActive('codeBlock')}
            onClick={() => editor.chain().focus().toggleCodeBlock().run()}
          />

          {/* TABLES */}
          <Toolbar.BlockSelector
            items={() => [
              {
                name: 'Insert Table 2x2',
                label: (
                  <div className="flex items-center gap-2">
                    <FaTable />
                    <span>Insert Table 2x2</span>
                  </div>
                ),
                // isActive: (editor) => editor.isActive('table'),
                isActive: 'default',
                setActive: (editor) =>
                  editor
                    .chain()
                    .focus()
                    .insertTable({ rows: 2, cols: 2, withHeaderRow: true })
                    .run(),
              },
              {
                name: 'Insert Table 3x3',
                label: (
                  <div className="flex items-center gap-2">
                    <FaTable />
                    <span>Insert Table 3x3</span>
                  </div>
                ),
                isActive: (editor) => editor.isActive('table'),
                setActive: (editor) =>
                  editor
                    .chain()
                    .focus()
                    .insertTable({ rows: 3, cols: 3, withHeaderRow: true })
                    .run(),
              },
              {
                name: 'Add Column Before',
                label: (
                  <div className="flex items-center gap-2">
                    <FaColumns />
                    <span>Add Column Before</span>
                  </div>
                ),
                isActive: (editor) => editor.isActive('table'),
                setActive: (editor) =>
                  editor.chain().focus().addColumnBefore().run(),
              },
              {
                name: 'Add Column After',
                label: (
                  <div className="flex items-center gap-2">
                    <FaColumns />
                    <span>Add Column After</span>
                  </div>
                ),
                isActive: (editor) => editor.isActive('table'),
                setActive: (editor) =>
                  editor.chain().focus().addColumnAfter().run(),
              },
              {
                name: 'Delete Column',
                label: (
                  <div className="flex items-center gap-2">
                    <FaMinus />
                    <span>Delete Column</span>
                  </div>
                ),
                isActive: (editor) => editor.isActive('table'),
                setActive: (editor) =>
                  editor.chain().focus().deleteColumn().run(),
              },
              {
                name: 'Add Row Before',
                label: (
                  <div className="flex items-center gap-2">
                    <FaPlus />
                    <span>Add Row Before</span>
                  </div>
                ),
                isActive: (editor) => editor.isActive('table'),
                setActive: (editor) =>
                  editor.chain().focus().addRowBefore().run(),
              },
              {
                name: 'Add Row After',
                label: (
                  <div className="flex items-center gap-2">
                    <FaPlus />
                    <span>Add Row After</span>
                  </div>
                ),
                isActive: (editor) => editor.isActive('table'),
                setActive: (editor) =>
                  editor.chain().focus().addRowAfter().run(),
              },
              {
                name: 'Delete Row',
                label: (
                  <div className="flex items-center gap-2">
                    <FaMinus />
                    <span>Delete Row</span>
                  </div>
                ),
                isActive: (editor) => editor.isActive('table'),
                setActive: (editor) => editor.chain().focus().deleteRow().run(),
              },
              {
                name: 'Delete Table',
                label: (
                  <div className="flex items-center gap-2">
                    <FaTrash />
                    <span>Delete Table</span>
                  </div>
                ),
                isActive: (editor) => editor.isActive('table'),
                setActive: (editor) =>
                  editor.chain().focus().deleteTable().run(),
              },
              {
                name: 'Merge Cells',
                label: (
                  <div className="flex items-center gap-2">
                    <FaObjectGroup />
                    <span>Merge Cells</span>
                  </div>
                ),
                isActive: (editor) => editor.isActive('table'),
                setActive: (editor) =>
                  editor.chain().focus().mergeCells().run(),
              },
              {
                name: 'Split Cell',
                label: (
                  <div className="flex items-center gap-2">
                    <FaObjectUngroup />
                    <span>Split Cell</span>
                  </div>
                ),
                isActive: (editor) => editor.isActive('table'),
                setActive: (editor) => editor.chain().focus().splitCell().run(),
              },
              {
                name: 'Toggle Header Column',
                label: (
                  <div className="flex items-center gap-2">
                    <FaHeading />
                    <span>Toggle Header Column</span>
                  </div>
                ),
                isActive: (editor) => editor.isActive('table'),
                setActive: (editor) =>
                  editor.chain().focus().toggleHeaderColumn().run(),
              },
              {
                name: 'Toggle Header Row',
                label: (
                  <div className="flex items-center gap-2">
                    <FaHeading />
                    <span>Toggle Header Row</span>
                  </div>
                ),
                isActive: (editor) => editor.isActive('table'),
                setActive: (editor) =>
                  editor.chain().focus().toggleHeaderRow().run(),
              },
              {
                name: 'Toggle Header Cell',
                label: (
                  <div className="flex items-center gap-2">
                    <FaHeading />
                    <span>Toggle Header Cell</span>
                  </div>
                ),
                isActive: (editor) => editor.isActive('table'),
                setActive: (editor) =>
                  editor.chain().focus().toggleHeaderCell().run(),
              },
              {
                name: 'Merge or Split',
                label: (
                  <div className="flex items-center gap-2">
                    <FaExpandArrowsAlt />
                    <span>Merge or Split</span>
                  </div>
                ),
                isActive: (editor) => editor.isActive('table'),
                setActive: (editor) =>
                  editor.chain().focus().mergeOrSplit().run(),
              },
              {
                name: 'Set Cell Attribute',
                label: (
                  <div className="flex items-center gap-2">
                    <span>⚙️</span>
                    <span>Set Cell Attribute</span>
                  </div>
                ),
                isActive: (editor) => editor.isActive('table'),
                setActive: (editor) =>
                  editor.chain().focus().setCellAttribute('colspan', 2).run(),
              },
              {
                name: 'Fix Tables',
                label: (
                  <div className="flex items-center gap-2">
                    <FaWrench />
                    <span>Fix Tables</span>
                  </div>
                ),
                isActive: (editor) => editor.isActive('table'),
                setActive: (editor) => editor.chain().focus().fixTables().run(),
              },
              {
                name: 'Go to Next Cell',
                label: (
                  <div className="flex items-center gap-2">
                    <FaArrowRight />
                    <span>Go to Next Cell</span>
                  </div>
                ),
                isActive: (editor) => editor.isActive('table'),
                setActive: (editor) =>
                  editor.chain().focus().goToNextCell().run(),
              },
              {
                name: 'Go to Previous Cell',
                label: (
                  <div className="flex items-center gap-2">
                    <FaArrowLeft />
                    <span>Go to Previous Cell</span>
                  </div>
                ),
                isActive: (editor) => editor.isActive('table'),
                setActive: (editor) =>
                  editor.chain().focus().goToPreviousCell().run(),
              },
            ]}
          />
          {/* HELP */}
          <Toolbar.Button
            name="Help"
            icon={<Icon.QuestionMark />}
            shortcut="CMD-H"
            onClick={() => {
              toast(
                <div className="flex flex-col items-start gap-2 text-sm">
                  <h3 className="font-bold">Need help?</h3>
                  <button
                    onClick={() => window.open('/docs')}
                    className="text-blue-500 hover:underline"
                  >
                    View Documentation →
                  </button>
                </div>,
                { duration: 7000 }
              );
            }}
          />
        </>
      }
    />
  );
}

export default CustomToolbar;
