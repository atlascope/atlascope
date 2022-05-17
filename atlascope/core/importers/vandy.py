import os

import pooch
import requests

from .base_importer import AtlascopeImporter


class VandyImporter(AtlascopeImporter):
    def perform_import(
        self,
        file_id: str,
        sha256sum: str,
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

        file_path = pooch.retrieve(
            url=f"https://styx.neurology.emory.edu/girder/api/v1/file/{file_id}/download",
            known_hash=f"sha256:{sha256sum}",
            downloader=pooch.HTTPDownloader(progressbar=True, headers=headers),
            fname=file_id,
        )

        # perform_import should save results to class attrs "content" and "metadata"
        self.content = open(file_path, "rb")
        self.metadata = {}
