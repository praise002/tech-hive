import { NodeViewWrapper, NodeViewContent } from '@tiptap/react';
import { useEffect, useState } from 'react';
import PropTypes from 'prop-types';

const languages = [
  { value: 'arduino', label: 'Arduino' },
  { value: 'bash', label: 'Bash' },
  { value: 'c', label: 'C' },
  { value: 'cpp', label: 'CPP' },
  { value: 'csharp', label: 'CSHARP' },
  { value: 'css', label: 'CSS' },
  { value: 'go', label: 'Go' },
  { value: 'java', label: 'Java' },
  { value: 'javascript', label: 'JavaScript' },
  { value: 'json', label: 'JSON' },
  { value: 'kotlin', label: 'Kotlin' },
  { value: 'makefile', label: 'MakeFile' },
  { value: 'markdown', label: 'Markdown' },
  { value: 'php', label: 'PHP' },
  { value: 'plaintext', label: 'Plaintext' },
  { value: 'python', label: 'Python' },
  { value: 'r', label: 'R' },
  { value: 'ruby', label: 'Ruby' },
  { value: 'rust', label: 'Rust' },
  { value: 'scss', label: 'SCSS' },
  { value: 'shell', label: 'Shell' },
  { value: 'sql', label: 'SQL' },
  { value: 'swift', label: 'Swift' },
  { value: 'typescript', label: 'TypeScript' },
  { value: 'xml', label: 'XML' },
  { value: 'yaml', label: 'YAML' },
];

export default function CodeBlockComponent({ node, updateAttributes }) {
  const [language, setLanguage] = useState(node.attrs.language);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  useEffect(() => {
    updateAttributes({ language });
  }, [language, updateAttributes]);

  function handleLanguageChange(lang) {
    setLanguage(lang);
    setIsDropdownOpen(false);
  }
  return (
    <NodeViewWrapper className="relative">
      {/* Language dropdown */}
      <div className="absolute right-2 top-2 z-10">
        <button
          type="button"
          onClick={(e) => {
            e.preventDefault();
            e.stopPropagation();
            setIsDropdownOpen((prev) => !prev);
          }}
          className="text-xs text-white bg-gray-800 border border-gray-300 rounded px-2 py-1 flex items-center gap-1"
        >
          {language}
          <svg
            className={`w-3 h-3 transition-transform ${
              isDropdownOpen ? 'rotate-180' : ''
            }`}
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M19 9l-7 7-7-7"
            />
          </svg>
        </button>

        {isDropdownOpen && (
          <div className="absolute right-0 mt-1 w-32 max-h-60 overflow-y-auto bg-gray-800 rounded-md shadow-lg border border-gray-700 z-20">
            {languages.map((lang) => (
              <button
                type="button"
                key={lang.value}
                onClick={(e) => {
                  e.preventDefault();
                  e.stopPropagation();
                  handleLanguageChange(lang.value);
                }}
                // text-left
                className={`block w-full px-3 py-1 text-left text-white text-xs hover:bg-gray-700 ${
                  language === lang.value ? 'bg-gray-700 font-medium' : ''
                }`}
              >
                {lang.label}
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Code content with default styling */}
      <pre className="!mt-2">
        <NodeViewContent as='code' />
      </pre>
    </NodeViewWrapper>
  );
}

CodeBlockComponent.propTypes = {
  node: PropTypes.shape({
    attrs: PropTypes.shape({
      language: PropTypes.string,
    }).isRequired,
  }).isRequired,
  updateAttributes: PropTypes.func.isRequired,
};
