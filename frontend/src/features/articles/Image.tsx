import Image from '@tiptap/extension-image';
import {
  NodeViewWrapper,
  NodeViewWrapperProps,
  ReactNodeViewRenderer,
} from '@tiptap/react';
import { useEffect, useRef, useState } from 'react';
import Button from '../../components/common/Button';
import Text from '../../components/common/Text';

function ImageNode(props: NodeViewWrapperProps) {
  const [isAltTextModalOpen, setIsAltTextModalOpen] = useState(false);
  const [altTextInput, setAltTextInput] = useState('');
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false);
  const [isImageSelected, setIsImageSelected] = useState(false);

  const { updateAttributes } = props;
  const { src, alt } = props.node.attrs;
  const nodeViewRef = useRef<HTMLDivElement>(null);
  // const { ...rest } = props.node.attrs;
  // console.log(rest);

  let className = 'image';
  if (props.selected) className += ' ProseMirror-selectednode ';

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (
        nodeViewRef.current &&
        !nodeViewRef.current.contains(event.target as Node)
      ) {
        setIsImageSelected(false);
      }
    }

    document.addEventListener('mousedown', handleClickOutside);

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  

  function handleAltTextInputChange(e: React.ChangeEvent<HTMLInputElement>) {
    setAltTextInput(e.target.value);
    setHasUnsavedChanges(e.target.value !== alt);
  }

  function handleSaveAltText() {
    updateAttributes({ alt: altTextInput });
    setHasUnsavedChanges(false);
    setIsAltTextModalOpen(false);
  }

  function handleOpenAltTextModal() {
    setAltTextInput(alt);
    setHasUnsavedChanges(false);
    setIsAltTextModalOpen(true);
  }

  function handleCloseAltTextModal() {
    if (hasUnsavedChanges) {
      const shouldDiscard = window.confirm(
        'You have unsaved changes. Do you want to discard them?'
      );
      if (!shouldDiscard) return;
    }

    setIsAltTextModalOpen(false);
    setAltTextInput('');
    setHasUnsavedChanges(false);
  }

  return (
    <>
      {/* TODO: FIX THE POS OF IS IMAGE SELECTED TEXT */}
      {/* center IMAGE */}
      <NodeViewWrapper
        className={className}
        data-drag-handle
        onClick={() => setIsImageSelected(true)}
        ref={nodeViewRef}
      >
        <div className="relative">
          <img src={src} alt={alt} />
          {isImageSelected && (
            <p className="absolute -top-15 left-[15%] bg-gray-500 text-white dark:bg-white/80 dark:text-black p-1 rounded text-sm flex items-center gap-2 z-10">
              {alt ? (
                <span className="font-bold text-green-500">✔</span>
              ) : (
                <span className="font-bold text-red-500">!</span>
              )}
              {alt ? (
                <span>Alt text: "{alt}".</span>
              ) : (
                <span>Alt text missing.</span>
              )}
              <button
                className="p-1 rounded cursor-pointer text-sm"
                type="button"
                onClick={handleOpenAltTextModal}
              >
                Edit
              </button>
            </p>
          )}
        </div>
      </NodeViewWrapper>

      {/* Modal Overlay */}
      {isAltTextModalOpen && (
        <div
          className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50"
          onClick={handleCloseAltTextModal} // Close modal when clicking outside
          role="dialog"
          aria-modal="true"
          aria-labelledby="modal-title"
        >
          {/* Modal Content */}
          <div
            className="bg-white w-full max-w-xl p-6 rounded-lg shadow-lg relative"
            onClick={(e) => e.stopPropagation()} // Prevent closing when clicking inside
          >
            <Text
              variant="h3"
              size="xl"
              bold={false}
              className="font-semibold text-gray-900 mb-4 !mt-0"
            >
              Alternative text
            </Text>
            <p className="text-gray-700 mb-6 text-sm">
              Write a brief description of this image for readers with visual
              impairments
            </p>

            <input
              type="text"
              value={altTextInput}
              onChange={handleAltTextInputChange}
              placeholder="Example: A cat sitting on a couch"
              className="text-sm appearance-none block w-full px-4 py-2 border border-gray-300 rounded-md focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-800 focus-visible:border-gray-800"
            />

            <div className="space-x-4 mt-4">
              <Button variant="outline" onClick={handleSaveAltText}>
                Save
              </Button>
              <Button onClick={handleCloseAltTextModal}>
                {hasUnsavedChanges ? 'Discard' : 'Cancel'}
              </Button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

export default Image.extend({
  addNodeView() {
    return ReactNodeViewRenderer(ImageNode);
  },
});
