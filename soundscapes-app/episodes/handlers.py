import feedparser
import pydub
import requests
from unipath import Path

from django.conf import settings
from django.core.files import File

def fetch_rss_entries(rss_url):
    feed = feedparser.parse(self.rss_url)
    return feed['entries']

def download_episode(downloadable_url):
    """ A URL from the media_content['url'] of an RSS entry.

    This function does not rename the file. It only downloads the file
    if the expected name is not present in the DOWNLOADS_DIR directory.

    Returns a django.core.files.File object that can be fed to a FileField.
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

def get_audio_duration(mp3):
    audio_segment = pydub.AudioSegment.from_mp3(mp3)
    return audio_segment.duration_seconds