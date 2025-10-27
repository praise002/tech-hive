# Fix for error in file uploading to cloudinary from ck editor
from cloudinary_storage.storage import MediaCloudinaryStorage

class CustomCloudinaryStorage(MediaCloudinaryStorage):
    def _save(self, name, content):
        # Reset file pointer to beginning
        content.seek(0)
        return super()._save(name, content)