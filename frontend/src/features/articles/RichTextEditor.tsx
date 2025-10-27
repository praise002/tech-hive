import { EditorProvider, ReactNodeViewRenderer } from '@tiptap/react';
import StarterKit from '@tiptap/starter-kit';

import Button from '../../components/common/Button';
import Text from '../../components/common/Text';

import MenuBar from './MenuBar';
import TextStyle from '@tiptap/extension-text-style';
import ListItem from '@tiptap/extension-list-item';
import CodeBlockLowlight from '@tiptap/extension-code-block-lowlight';
import { common, createLowlight } from 'lowlight';

import Color from '@tiptap/extension-color';
import Image from '@tiptap/extension-image';
import Table from '@tiptap/extension-table';
import TableRow from '@tiptap/extension-table-row';
import TableHeader from '@tiptap/extension-table-header';
import TableCell from '@tiptap/extension-table-cell';
import Youtube from '@tiptap/extension-youtube';
import Link from '@tiptap/extension-link';
import TextAlign from '@tiptap/extension-text-align';
import Placeholder from '@tiptap/extension-placeholder';
import Typography from '@tiptap/extension-typography';
import BubbleMenuFromProvider from './BubbleMenuFromProvider';
import FloatingMenuFromProvider from './FloatingMenuFromProvider';
import ArticleMetadata from './ArticleMetadata';

import CodeBlockComponent from './CodeBlockComponent';

// create a lowlight instance with all languages loaded or use common
const lowlight = createLowlight(common);

const extensions = [
  TextStyle.configure({
    types: [ListItem.name],
  } as any), // tells the color to work with ListItem: any: tells ts to trust me
  Color,
  Image,
  TableRow,
  TableHeader,
  TableCell,
  Typography,
  StarterKit.configure({
    // Disable the default CodeBlock extension
    codeBlock: false,
  }),
  Table.configure({
    resizable: true,
  }),
  Placeholder.configure({
    placeholder: 'Write something …',
  }),
  TextAlign.configure({
    types: ['heading', 'paragraph'],
    alignments: ['left', 'center'],
  }),
  // CodeBlockLowlight.configure({
  //   lowlight,
  //   defaultLanguage: 'javascript',

  // }),
  CodeBlockLowlight.extend({
    addNodeView() {
      return ReactNodeViewRenderer(CodeBlockComponent); // This connects React to Tiptap
    },
  }).configure({
    lowlight,
    defaultLanguage: 'javascript',
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
];

let content = `<h2>Heading</h2>
        <p style="text-align: center">first paragraph</p>
        <p style="text-align: left">second paragraph</p>
        <p>“I have been suffering from Typomania all my life, a sickness that is incurable but not lethal.”</p>
        <p>— Erik Spiekermann, December 2008</p>
        <pre><code class="language-javascript">const foo = "bar"</code></pre>
      <pre><code class="language-css">body { color: red }</code></pre>
      <pre><code class="language-python">name = "bar"</code></pre>
      <img src="https://placehold.co/800x400" />
      <table>
          <tbody>
            <tr>
              <th>Name</th>
              <th colspan="3">Description</th>
            </tr>
            <tr>
              <td>Cyndi Lauper</td>
              <td>Singer</td>
              <td>Songwriter</td>
              <td>Actress</td>
            </tr>
          </tbody>
        </table>
        <div data-youtube-video>
        <iframe src="https://www.youtube.com/watch?v=3lTUAWOgoHs"></iframe>
      </div>
      <p>
          Wow, this editor has support for links to the whole <a href="https://en.wikipedia.org/wiki/World_Wide_Web">world wide web</a>. We tested a lot of URLs and I think you can add *every URL* you want. Isn’t that cool? Let’s try <a href="https://statamic.com/">another one!</a> Yep, seems to work.
        </p>`;

content = '';

function RichTextEditor() {
  // Show contributor's Dashboard depending on who logged in using auth later
  return (
    <div className="py-20 px-4 sm:px-6 lg:px-8">
      <Text
        variant="h1"
        size="lg"
        bold={false}
        className="font-semibold mb-1 text-gray-900 dark:text-custom-white"
      >
        Techive&apos;s Dashboard
      </Text>
      <div className="flex items-center gap-2 my-4 dark:text-custom-white">
        <button className="text-secondary focus-visible:outline-0 focus-visible:ring-2 transition duration-300">
          Edit
        </button>
        <div className="h-4 w-[1px] bg-red"></div>
        <button className="font-semibold focus-visible:outline-0 focus-visible:ring-2 transition duration-300">
          Preview
        </button>
      </div>

      <ArticleMetadata mode="edit" />

      <div className="w-full">
        <EditorProvider
          slotBefore={<MenuBar />}
          extensions={extensions}
          content={content}
          editable={true} // to allow bubble bar display
          editorProps={{
            attributes: {
              class:
                'mt-2 w-full max-w-none focus:outline-none border border-gray-800 dark:border-custom-white rounded-md px-2 min-h-[300px] prose md:prose-lg lg:prose-xl dark:prose-invert',
            },
          }}
        >
          {/* It has to be inside for it to work */}
          <BubbleMenuFromProvider />
          <FloatingMenuFromProvider />
        </EditorProvider>
      </div>

      <div className="flex gap-2 mt-5">
        <Button variant="outline">Save as Draft</Button>
        <Button>Publish</Button>
      </div>
    </div>
  );
}
// for admin and contributor, change the title based on the role
export default RichTextEditor;
