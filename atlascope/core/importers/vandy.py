import io
import os
import requests

from atlascope.core.importers import AtlascopeImporter


class VandyImporter(AtlascopeImporter):
    def perform_import(
        self,
        source_uri: str = None,
        api_key: str = None,
        token_url: str = None,
    ):
        api_key = api_key or os.environ.get("DJANGO_API_TOKEN")
        if not source_uri or not api_key or not token_url:
            self.raise_schema_exception()

        params = {"key": api_key}
        token = requests.post(token_url, params=params).json()["authToken"]["token"]
        headers = {"girder-token": token}

        r = requests.get(source_uri, headers=headers, stream=True)

        # perform_import should save results to class attrs "content" and "metadata"
        self.content = io.BytesIO(r.content)
        self.metadata = {}
