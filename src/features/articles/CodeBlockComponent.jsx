import { NodeViewWrapper } from '@tiptap/react';

const CodeBlockComponent = (node, updateAttributes) => {
  const language = node.attrs.language;

  return (
    <NodeViewWrapper className="code-block">
      <select
        contentEditable={false}
        defaultValue={language}
        onChange={(e) => updateAttributes({ language: e.target.value })}
        className="language-select"
      >
        <option value="javascript">JavaScript</option>
        <option value="typescript">TypeScript</option>
        <option value="python">Python</option>
        <option value="css">CSS</option>
        <option value="html">HTML</option>
      </select>
    </NodeViewWrapper>
  );
}

export default CodeBlockComponent;
