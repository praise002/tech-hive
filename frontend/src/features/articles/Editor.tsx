'use client';

import {
  useLiveblocksExtension,
  FloatingToolbar,
} from '@liveblocks/react-tiptap';
import { useEditor, EditorContent } from '@tiptap/react';
import StarterKit from '@tiptap/starter-kit';
import { Threads } from './Threads';

export function Editor() {
  const liveblocks = useLiveblocksExtension();

  const editor = useEditor({
    extensions: [
      liveblocks,
      StarterKit.configure({
        // The Liveblocks extension comes with its own history handling
        history: false,
      }),
    ],
    content: '<p>Start typing here...</p>', // Add initial content
    editorProps: {
      attributes: {
        class: 'prose prose-sm sm:prose lg:prose-lg xl:prose-2xl mx-auto focus:outline-none',
      },
    },
  });

  return (
    <div className='mt-20 bg-white min-h-screen p-6'>
      <div className="max-w-4xl mx-auto">
        <div className="border border-gray-300 rounded-lg min-h-96 p-4">
          <EditorContent 
            editor={editor} 
            className="editor min-h-64 focus-within:outline-none" 
          />
        </div>
        <Threads editor={editor} />
        <FloatingToolbar editor={editor} />
      </div>
    </div>
  );
}