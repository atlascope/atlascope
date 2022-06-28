from .gdrive import GoogleDriveImporter
from .upload import UploadImporter
from .vandy import VandyImporter

available_importers = {
    cls.__name__: cls
    for cls in [
        UploadImporter,
        VandyImporter,
        GoogleDriveImporter,
    ]
}
