import Button from "../../components/common/Button";

function RichTextEditor() {
  return (
    <div className="my-40 mx-auto">
      <div>Others</div>
      <div className="flex gap-2">
        <Button variant="outline">Save as Draft</Button>
        <Button>Publish</Button>
      </div>
    </div>
  );
}

export default RichTextEditor;
