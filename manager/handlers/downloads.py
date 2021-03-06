import requests
from unipath import Path

from django.conf import settings
from django.core.files import File

def download_file(downloadable_url):
    """ File is only downloaded if it doesn't exist in DOWNLOADS_DIR

    This function does not rename the file. It only downloads the file
    if the expected name is not present in the DOWNLOADS_DIR.

    Returns a django.core.files.File object that can be stored in a FileField.
    """
    download_dir = Path(settings.DOWNLOADS_DIR)
    if not download_dir.exists():
        download_dir.mkdir()

    name_in_url = Path(downloadable_url).name
    expected_loc = Path(download_dir, name_in_url)

    # only download if necessary
    if not expected_loc.exists():
        response = requests.get(downloadable_url, stream = True)
        with open(expected_loc, 'wb') as expected_loc_handle:
            for chunk in response.iter_content(chunk_size = 1024):
                expected_loc_handle.write(chunk)

    return File(open(expected_loc, 'rb'))
