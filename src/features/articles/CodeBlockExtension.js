// CodeBlockExtension.js
import { Node } from '@tiptap/core';
import { ReactNodeViewRenderer } from '@tiptap/react';
import CodeBlockComponent from './CodeBlockComponent';


export const CodeBlockExtension = Node.create({
  name: 'codeBlock',
  group: 'block',
  content: 'text*',
  marks: '',
  defining: true,
  code: true,
  isolating: true,

  addAttributes() {
    return {
      language: {
        default: 'javascript',
      },
    };
  },

  parseHTML() {
    return [
      {
        tag: 'pre',
        preserveWhitespace: 'full',
        getAttrs: (node) => ({
          language: node.querySelector('code')?.getAttribute('class')?.replace('language-', '') || 'javascript',
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
        0,
      ],
    ];
  },

  addCommands() {
    return {
      toggleCodeBlock: () => ({ commands }) => {
        return commands.toggleNode('codeBlock', 'paragraph');
      },
      setCodeBlock: () => ({ commands }) => {
        return commands.setNode('codeBlock');
      },
    };
  },

  addNodeView() {
    return ReactNodeViewRenderer(CodeBlockComponent);
  },
});