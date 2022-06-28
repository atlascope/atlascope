import pooch
import requests

from .base_importer import AtlascopeImporter


class GoogleDriveImporter(AtlascopeImporter):
    def get_confirm_token(self, response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value

        return None

    def perform_import(
        self,
        file_id: str,
        sha256sum: str,
    ):
        url_base = "https://docs.google.com/uc?export=download"
        params = {'id': file_id}
        session = requests.Session()
        response = session.get(url_base, params=params, stream=True)
        token = self.get_confirm_token(response)
        params['confirm'] = token

        try:
            file_path = pooch.retrieve(
                url=url_base,
                known_hash=f"sha256:{sha256sum}",
                downloader=pooch.HTTPDownloader(progressbar=True, params=params),
                fname=file_id,
            )

            # perform_import should save results to class attrs "content" and "metadata"
            self.content = open(file_path, "rb")
            self.metadata = {}
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                print('Exceeded maximum Google Drive download requests. Try again later.')
