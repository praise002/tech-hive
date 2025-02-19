import { useState } from "react";
import Button from "../components/common/Button";
import Text from "../components/common/Text";

function EditorDashboard() {
  const [isEditorOpen, setIsEditorOpen] = useState(false);

  const handleAddPostClick = () => {
    setIsEditorOpen(true);
  };

  return (
    <div className="p-8">
      {/* Header */}
      <Text variant="h2" size="xl" className="mb-6 font-semibold">
        Admin Dashboard
      </Text>

      {/* Post List */}
      <div className="mb-6">
        <Text variant="h3" size="lg" className="mb-4 font-semibold">
          Posts
        </Text>
        <table className="w-full border-collapse">
          <thead>
            <tr>
              <th className="border p-2">Title</th>
              <th className="border p-2">Author</th>
              <th className="border p-2">Status</th>
              <th className="border p-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            {/* Example Post Row */}
            <tr>
              <td className="border p-2">How to Use React</td>
              <td className="border p-2">John Doe</td>
              <td className="border p-2">Published</td>
              <td className="border p-2">
                <Button variant="outline" onClick={() => alert('Edit Post')}>
                  Edit
                </Button>
                <Button
                  variant="outline"
                  className="ml-2"
                  onClick={() => alert('Delete Post')}
                >
                  Delete
                </Button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      {/* Add Post Button */}
      <Button variant="gradient" onClick={handleAddPostClick}>
        Add New Post
      </Button>

      {/* Markdown Editor (conditionally rendered) */}
      {/* {isEditorOpen && (
        <MarkdownEditor onClose={() => setIsEditorOpen(false)} />
      )} */}
    </div>
  );
}

export default EditorDashboard;
