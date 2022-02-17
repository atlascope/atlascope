import io
import os

import requests

from .base_importer import AtlascopeImporter


class VandyImporter(AtlascopeImporter):
    def perform_import(
        self,
        file_id: str,
        api_key: str = None,
    ):
        api_key = api_key or os.environ.get("DJANGO_API_TOKEN")
        if not api_key:
            self.raise_schema_exception()

        params = {"key": api_key}
        token_url = "https://styx.neurology.emory.edu/girder/api/v1/api_key/token"
        token_res = requests.post(token_url, params=params).json()
        if 'authToken' not in token_res:
            return

        token = token_res["authToken"]["token"]
        headers = {"girder-token": token}

        source_url = f"https://styx.neurology.emory.edu/girder/api/v1/file/{file_id}/download"
        r = requests.get(source_url, headers=headers, stream=True)

        # perform_import should save results to class attrs "content" and "metadata"
        self.content = io.BytesIO(r.content)
        self.metadata = {}
