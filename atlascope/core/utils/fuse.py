from pathlib import Path
import fsspec
from urllib.error import HTTPError
from urllib.parse import urlparse
from urllib.request import urlopen


def precheck_fuse(url: str) -> bool:
    try:
        import simple_httpfs  # noqa
    except (ImportError, EnvironmentError):
        return False
    parsed = urlparse(url)
    if parsed.scheme not in ['https', 'http']:
        return False
    try:
        # The FUSE lib will not catch URL errors
        with urlopen(url):
            return True
    except HTTPError:
        return False


def url_file_to_fuse_path(url: str) -> Path:
    parsed = urlparse(url)
    if parsed.scheme in ['https', 'http']:
        fuse_path = url.replace(f'{parsed.scheme}://', '/data') + '..'
    elif parsed.scheme == 's3':
        fuse_path = url.replace('s3://', '/data') + '..'
    else:
        raise ValueError(f'Scheme {parsed.scheme} not currently handled by FUSE.')
    return Path(fuse_path)


def remote_dataset_to_local_path(dataset):
    """Create a local path for a dataset's remote content.
    This will first attempt to use httpfs to FUSE mount the file's URL.
    If FUSE is unavailable, this will fallback to downloading the entire
    file to local storage.
    """
    url = dataset.content.url
    root = Path('/', 'data')
    path = root / str(dataset.id)
    if precheck_fuse(url):
        return url_file_to_fuse_path(url)
    # Fallback to loading entire file locally
    cached = fsspec.open_local(
        f'simplecache::{url}',
        filecache={'cache_storage': path},
    )
    return cached[0]
