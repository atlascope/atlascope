from .upload import UploadImporter
from .vandy import VandyImporter
from .gdrive import GoogleDriveImporter

available_importers = {
    cls.__name__: cls
    for cls in [
        UploadImporter,
        VandyImporter,
        GoogleDriveImporter,
    ]
}
