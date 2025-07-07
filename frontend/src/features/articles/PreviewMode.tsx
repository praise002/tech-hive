import { AnyExtension, EditorContent, useEditor } from '@tiptap/react';

import { useMemo } from 'react';

function PreviewMode({
  content,
  extensions,
}: {
  content: string;
  extensions: AnyExtension[];
}) {
  const initialContent = () => {
    try {
      JSON.parse(content);
    } catch (error) {
      console.error('Failed to parse editor content:', error);
      // Return a valid empty document structure
      return {
        type: 'doc',
        content: [
          {
            type: 'paragraph',
            content: [{ type: 'text', text: 'Preview unavailable' }],
          },
        ],
      };
    }
  };

  const editor = useEditor({
    editable: false, // Disables editing
    extensions: useMemo(() => extensions, [extensions]),
    content: useMemo(() => initialContent, [initialContent]), // Converts JSON into an obj
  });

  return (
    <div className="prose md:prose-lg lg:prose-xl max-w-none dark:prose-invert">
      <EditorContent editor={editor} className="editor" />
    </div>
  );
}

export default PreviewMode;
