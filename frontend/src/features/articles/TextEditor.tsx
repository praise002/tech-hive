'use client';

import {
  useLiveblocksExtension,
  FloatingToolbar,
} from '@liveblocks/react-tiptap';
import { useEditor, EditorContent, ReactNodeViewRenderer } from '@tiptap/react';
import StarterKit from '@tiptap/starter-kit';
import { Threads } from './Threads';
import Youtube from '@tiptap/extension-youtube';

import CustomToolbar from './CustomToolbar';
import { ClientSideSuspense } from '@liveblocks/react';
import TableRow from '@tiptap/extension-table-row';
import TableHeader from '@tiptap/extension-table-header';
import TableCell from '@tiptap/extension-table-cell';
import Table from '@tiptap/extension-table';
import TextAlign from '@tiptap/extension-text-align';
import Link from '@tiptap/extension-link';

import Placeholder from '@tiptap/extension-placeholder';
import CodeBlockLowlight from '@tiptap/extension-code-block-lowlight';
import { common, createLowlight } from 'lowlight';
import CodeBlockComponent from './CodeBlockComponent';
import Typography from '@tiptap/extension-typography';
import Text from '../../components/common/Text';
import ArticleMetadata from './ArticleMetadata';
import Button from '../../components/common/Button';
import { useState } from 'react';
import PreviewMode from './PreviewMode';
import Dropcursor from '@tiptap/extension-dropcursor';
import Image from './Image';
import toast from 'react-hot-toast';

// create a lowlight instance with all languages loaded or use common
const lowlight = createLowlight(common);

function TextEditor() {
  const [mode, setMode] = useState<'edit' | 'preview'>('edit');
  const [editorContent, setEditorContent] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const liveblocks = useLiveblocksExtension();

  const editor = useEditor({
    extensions: [
      ...(mode === 'edit' ? [liveblocks] : []),

      StarterKit.configure({
        // The Liveblocks extension comes with its own history handling
        history: false,
      }),

      Placeholder.configure({
        placeholder: 'Write something …',
      }),
      CodeBlockLowlight.extend({
        addNodeView() {
          return ReactNodeViewRenderer(CodeBlockComponent); // This connects React to Tiptap
        },
      }).configure({
        lowlight,
        defaultLanguage: 'javascript',
      }),
      Table.configure({
        resizable: true,
      }),
      Image,
      Dropcursor,
      Typography,
      TableRow,
      TableHeader,
      TableCell,
      TextAlign.configure({
        types: ['heading', 'paragraph'],
        alignments: ['left', 'center'],
      }),
      Youtube.configure({
        controls: false,
        nocookie: true,
      }),
      Link.configure({
        openOnClick: false,
        defaultProtocol: 'https',
        protocols: ['http', 'https'],
        isAllowedUri: (url, ctx) => {
          try {
            // construct URL
            const parsedUrl = url.includes(':')
              ? new URL(url)
              : new URL(`${ctx.defaultProtocol}://${url}`);

            // use default validation
            if (!ctx.defaultValidate(parsedUrl.href)) {
              return false;
            }

            // disallowed protocols
            const disallowedProtocols = ['ftp', 'file', 'mailto'];
            const protocol = parsedUrl.protocol.replace(':', '');

            if (disallowedProtocols.includes(protocol)) {
              return false;
            }

            // only allow protocols specified in ctx.protocols
            const allowedProtocols = ctx.protocols.map((p) =>
              typeof p === 'string' ? p : p.scheme
            );

            if (!allowedProtocols.includes(protocol)) {
              return false;
            }

            // disallowed domains
            const disallowedDomains = [
              'example-phishing.com',
              'malicious-site.net',
            ];
            const domain = parsedUrl.hostname;

            if (disallowedDomains.includes(domain)) {
              return false;
            }

            // all checks have passed
            return true;
          } catch {
            return false;
          }
        },
        shouldAutoLink: (url) => {
          try {
            // construct URL
            const parsedUrl = url.includes(':')
              ? new URL(url)
              : new URL(`https://${url}`);

            // only auto-link if the domain is not in the disallowed list
            const disallowedDomains = [
              'example-no-autolink.com',
              'another-no-autolink.com',
            ];
            const domain = parsedUrl.hostname;

            return !disallowedDomains.includes(domain);
          } catch {
            return false;
          }
        },
      }),
    ],

    editorProps: {
      attributes: {
        class:
          'mt-5 w-full max-w-none focus:outline-none border border-gray-800 rounded-md dark:border-custom-white dark:text-white px-3 mx-2 min-h-[300px] prose md:prose-lg lg:prose-xl dark:proae-invert',
      },
      // handleDrop: function (view, event, slice, moved) {
      handleDrop: function (view, event, _slice, moved) {
        if (!moved && event.dataTransfer?.files?.length) {
          const files = Array.from(event.dataTransfer.files);
          const coordinates = view.posAtCoords({
            left: event.clientX,
            top: event.clientY,
          });
          if (!coordinates) return false;

          files.forEach((file, index) => {
            const fileSize = parseFloat((file.size / 1024 / 1024).toFixed(4)); // get the filesize in MB
            if (
              !['image/jpeg', 'image/png'].includes(file.type) ||
              fileSize >= 10
            ) {
              toast.error(`Skipped: ${file.name} - Must be JPG/PNG under 10MB`);
              return; // skip this file
            }

            const _URL = window.URL || window.webkitURL;
            const url = _URL.createObjectURL(file);
            const img = new window.Image();

            img.onload = function (e: Event) {
              const imgElement = e.target as HTMLImageElement;
              if (imgElement.width > 5000 || imgElement.height > 5000) {
                toast.error(`Skipped: ${file.name} - Dimensions exceed 5000px`);
                URL.revokeObjectURL(url);
                return;
              }

              // Calculate position with offset for multiple images
              const insertPos = coordinates.pos + index;
              const { schema } = view.state;
              const node = schema.nodes.image.create({
                src: url,
                alt: `Image ${index + 1}`,
              }); // creates the image element
              const transaction = view.state.tr.insert(insertPos, node); // places it in the correct position
              view.dispatch(transaction);
              URL.revokeObjectURL(url);
            };

            img.onerror = () => {
              toast.error(`Failed to load: ${file.name}`);
            };

            img.src = url;
          });

          return true; // handled
        }
        return false; // not handled use default behaviour
      },
    },
  });

  return (
    <div className="py-24 px-4 sm:px-6 lg:px-8">
      <Text
        variant="h1"
        size="lg"
        bold={false}
        className="font-semibold mb-1 text-gray-900 dark:text-custom-white"
      >
        {/* Techive&apos;s Dashboard */}
        {isLoading ? 'Loading Preview' : "Techive's Dashboard"}
      </Text>
      <div className="flex items-center gap-2 my-4 dark:text-custom-white">
        <button
          onClick={() => setMode('edit')}
          className={`${
            mode === 'edit' ? 'font-semibold' : 'text-secondary'
          } cursor-pointer focus-visible:outline-0 focus-visible:ring-2 transition duration-300`}
        >
          Edit
        </button>
        <div className="h-4 w-[1px] bg-red"></div>
        <button
          onClick={() => {
            setIsLoading(true);
            setEditorContent(JSON.stringify(editor?.getJSON())); // Save content
            setMode('preview');
            setTimeout(() => setIsLoading(false), 2000); // TODO: REMOVE LATER
          }}
          className={`${
            mode === 'preview' ? 'font-semibold' : 'text-secondary'
          } cursor-pointer focus-visible:outline-0 focus-visible:ring-2 transition duration-300`}
        >
          Preview
        </button>
      </div>

      {mode == 'edit' ? (
        <>
          <ArticleMetadata mode="edit" />
          <CustomToolbar editor={editor} />
          <EditorContent editor={editor} className="editor" />

          {/* To prevent it from rendering until threads are loaded */}
          <ClientSideSuspense fallback={null}>
            <Threads editor={editor} />
          </ClientSideSuspense>
          <FloatingToolbar editor={editor} />
        </>
      ) : (
        <>
          <ArticleMetadata mode="preview" />
          <PreviewMode
            content={editorContent}
            extensions={editor?.options?.extensions || []}
          />
        </>
      )}

      <div className="flex gap-2 mt-5">
        <Button variant="outline">Save as Draft</Button>
        <Button>Publish</Button>
      </div>
    </div>
  );
}

export default TextEditor;
