function Docs() {
  return (
    <div className="mt-15 max-w-3xl mx-auto p-4 md:p-8 bg-white rounded-lg shadow-lg text-gray-800">
    <h1 className="text-3xl font-bold mb-4 text-blue-700">
      TechHive Editor Help Docs
    </h1>
    <p className="mb-6 text-lg">
      Welcome to the TechHive collaborative editor! Here’s how to make the most
      of your editing experience.
    </p>

    {/* Section: Collaborative Editing */}
    <section className="mb-8">
      <h2 className="text-xl font-semibold mb-2 text-blue-600">
        Real-Time Collaboration
      </h2>
      <ul className="list-disc pl-6 space-y-2">
        <li>
          Work together with your team in real-time. Changes are instantly
          synced for all participants.
        </li>
        <li>See other users’ cursors and selections as you edit.</li>
        <li className="text-sm text-gray-500">
          Tip: If you notice lag or syncing issues, check your internet
          connection.
        </li>
      </ul>
    </section>

    {/* Section: Basic Editing */}
    <section className="mb-8">
      <h2 className="text-xl font-semibold mb-2 text-blue-600">
        Basic Editing
      </h2>
      <ul className="list-disc pl-6 space-y-2">
        <li>
          Use the toolbar to format text (bold, italic, headings, lists, etc.).
        </li>
        <li>
          Undo/redo changes using the toolbar or{' '}
          <span className="font-mono bg-gray-100 px-1 rounded">Ctrl+Z</span> /{' '}
          <span className="font-mono bg-gray-100 px-1 rounded">Ctrl+Y</span>.
        </li>
        <li>
          Click anywhere in the document to move your cursor and start typing.
        </li>
      </ul>
    </section>

    {/* Section: Images */}
    <section className="mb-8">
      <h2 className="text-xl font-semibold mb-2 text-blue-600">
        Working with Images
      </h2>
      <ul className="list-disc pl-6 space-y-2">
        <li>
          Click on an image to select it. A floating{' '}
          <span className="font-semibold">"Add Alt Text"</span> button will
          appear above the image.
        </li>
        <li>
          Click <span className="font-semibold">"Add Alt Text"</span> to open a
          modal and describe the image for accessibility.
        </li>
        <li>
          The tooltip stays attached to the image, even if you move or resize
          it.
        </li>
        <li className="text-sm text-gray-500">
          Tip: Alt text helps visually impaired users understand your content.
        </li>
      </ul>
    </section>

    {/* Section: Navigation & Troubleshooting */}
    <section className="mb-8">
      <h2 className="text-xl font-semibold mb-2 text-blue-600">
        Navigation & Troubleshooting
      </h2>
      <ul className="list-disc pl-6 space-y-2">
        <li>
          If you get lost, use the <span className="font-semibold">Home</span>{' '}
          or <span className="font-semibold">Dashboard</span> links to return to
          the main page.
        </li>
        <li>If the editor seems unresponsive, try refreshing the page.</li>
        <li className="text-sm text-gray-500">
          For persistent issues, contact support or check your browser
          compatibility.
        </li>
      </ul>
    </section>

    {/* Section: Accessibility */}
    <section className="mb-8">
      <h2 className="text-xl font-semibold mb-2 text-blue-600">
        Accessibility
      </h2>
      <ul className="list-disc pl-6 space-y-2">
        <li>Use descriptive alt text for all images.</li>
        <li>
          Structure your content with headings and lists for easier reading.
        </li>
      </ul>
    </section>

    {/* Section: FAQ */}
    <section className="mb-8">
      <h2 className="text-xl font-semibold mb-2 text-blue-600">
        Frequently Asked Questions
      </h2>
      <ul className="list-disc pl-6 space-y-2">
        <li>
          <span className="font-semibold">Q:</span> How do I add an image?
          <br />
          <span className="font-semibold">A:</span> Use the toolbar’s image
          button or drag-and-drop an image into the editor.
        </li>
        <li>
          <span className="font-semibold">Q:</span> How do I edit alt text?
          <br />
          <span className="font-semibold">A:</span> Click the image, then click
          the floating "Add Alt Text" button.
        </li>
        <li>
          <span className="font-semibold">Q:</span> Can I see who else is
          editing?
          <br />
          <span className="font-semibold">A:</span> Yes, you'll see other users'
          cursors and selections in real-time.
        </li>
      </ul>
    </section>

    <footer className="mt-8 text-center text-sm text-gray-400">
      Need more help? Contact
      support.
    </footer>
  </div>
  )
}

export default Docs;
