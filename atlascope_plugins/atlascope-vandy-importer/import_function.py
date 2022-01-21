import requests
import io
import os


def run(source_uri=None):
    params = {'key': os.environ.get('DJANGO_API_TOKEN')}
    tokenUrl = "https://styx.neurology.emory.edu/girder/api/v1/api_key/token"

    token = requests.post(tokenUrl, params=params).json()["authToken"]["token"]

    headers = {'girder-token': token}

    r = requests.get(source_uri, headers=headers, stream=True)

    imported_file = io.BytesIO(r.content)

    return imported_file
