'use client';

import {
  useLiveblocksExtension,
  FloatingToolbar,
} from '@liveblocks/react-tiptap';
import { useEditor, EditorContent } from '@tiptap/react';
import StarterKit from '@tiptap/starter-kit';
import { Threads } from './Threads';

import CustomToolbar from './CustomToolbar';
import { ClientSideSuspense } from '@liveblocks/react';
import TableRow from '@tiptap/extension-table-row';
import TableHeader from '@tiptap/extension-table-header';
import TableCell from '@tiptap/extension-table-cell';
import Table from '@tiptap/extension-table';
import TextAlign from '@tiptap/extension-text-align';

export function Editor() {
  const liveblocks = useLiveblocksExtension();

  const editor = useEditor({
    extensions: [
      liveblocks,

      StarterKit.configure({
        // The Liveblocks extension comes with its own history handling
        history: false,
      }),
      Table.configure({
        resizable: true,
      }),
      TableRow,
      TableHeader,
      TableCell,
      TextAlign.configure({
        types: ['heading', 'paragraph'],
        alignments: ['left', 'center'],
      }),
    ],
    editorProps: {
      attributes: {
        class:
          'mt-5 w-full max-w-none focus:outline-none border border-gray-800 rounded-md dark:border-none dark:bg-white px-2 mx-2 min-h-[300px] prose md:prose-lg lg:prose-xl ',
      },
    },
  });

  return (
    <div className="mt-24">
      {/* <Toolbar editor={editor} /> */}

      <CustomToolbar editor={editor} />
      <EditorContent editor={editor} className="editor" />
      {/* To prevent it from rendering until threads are loaded */}
      <ClientSideSuspense fallback={null}>
        <Threads editor={editor} />
      </ClientSideSuspense>

      <FloatingToolbar editor={editor} />
    </div>
  );
}
