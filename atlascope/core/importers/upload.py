import io

from atlascope.core.importers import AtlascopeImporter


class UploadImporter(AtlascopeImporter):
    def perform_import(self, content: bytes, metadata: dict):
        self.content = io.BytesIO(content)
        self.metadata = metadata or {}
