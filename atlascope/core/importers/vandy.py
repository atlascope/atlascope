from atlascope.core.importers import AtlascopeImporter


class VandyImporter(AtlascopeImporter):
    def perform_import(
        self,
        source_uri: str,
        api_key: str,
        token_url: str,
    ):
        api_key = api_key or os.environ.get("DJANGO_API_TOKEN")
        params = {"key": api_key}
        # token_url = "https://styx.neurology.emory.edu/girder/api/v1/api_key/token"

        token = requests.post(token_url, params=params).json()["authToken"]["token"]

        headers = {"girder-token": token}

        r = requests.get(source_uri, headers=headers, stream=True)

        imported_file = io.BytesIO(r.content)

        return imported_file
