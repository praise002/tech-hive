import { Node } from '@tiptap/core';
import { ReactNodeViewRenderer } from '@tiptap/react';
import CodeBlockComponent from './CodeBlockComponent';

// STEP 1: CREATE A NODE EXTENSION
export const CodeBlockExtension = Node.create({
  name: 'CodeBlock',
  group: 'block', // block-level element
  content: 'text*', // Can contain text
  marks: '', // No bold/italic inside code blocks
  defining: true, // treat it as one unit
  code: true,
  isolating: true, // treat it as one unit

  parseHTML() {
    return [
      {
        tag: 'pre',
        preserveWhitespace: 'full',
        getAttrs: (node) => ({
          language: node
            .querySelector('code')
            ?.getAttribute('class')
            ?.replace('language-', ''),
        }),
      },
    ];
  },

  renderHTML({ HTMLAttributes }) {
    return [
      'pre',
      {},
      [
        'code',
        {
          class: `language-${HTMLAttributes.language}`,
        },
        0, // placeholder for the actual code content
      ],
    ];
  },

  addCommands() {
    return {
      toggleCodeBlock:
        () =>
        ({ commands }) => {
          return commands.toggleNode('codeBlock', 'paragraph');
        }, // turns a paragraph into a code block
      setCodeBlock: () => () => {
        return this.editor.commands.setNode('codeBlock');
      },
    };
  },

  addNodeView() {
    return ReactNodeViewRenderer(CodeBlockComponent);
  }, // connects React component to tiptap
});
