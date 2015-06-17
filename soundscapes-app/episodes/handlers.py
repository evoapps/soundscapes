from unipath import Path

# RSS handling
import feedparser
import json
import requests

# mp3 handling
import pydub
from math import floor
from noise import pnoise1

from django.conf import settings
from django.core.files import File

def fetch_rss_entries(rss_url, n = None):
    """ Retrieve entries from an RSS feed

    n: the number of recent episodes to return

    Defaults to returning the full feed.
    """
    feed = feedparser.parse(rss_url)
    entries = feed['entries']
    n = n or len(entries)
    return entries[0:n]

def dump_rss_entry(rss_entry):
    # hack! "json.dumps(rss_entry)" chokes on time object
    modified_rss_entry = rss_entry.copy()
    modified_rss_entry['published_parsed'] = \
        str(modified_rss_entry['published_parsed'])
    return json.dumps(modified_rss_entry)

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

def get_audio_duration(mp3_file):
    audio_segment = pydub.AudioSegment.from_mp3(mp3_file)
    return audio_segment.duration_seconds

def get_audio_features(mp3_file):
    """ (MOCKED) Extract (x,y) pairs from an mp3

    MOCKED: right now only random numbers are generated

    TODO: implement sampling_rate parameter
    """
    audio_segment = pydub.AudioSegment.from_mp3(mp3_file)
    duration = int(floor(audio_segment.duration_seconds))

    xy_data = list()

    for time in xrange(duration):
        # hack! transform of x is only because I don't understand pnoise1
        x = float(time)/duration
        y = pnoise1(x, octaves = 1)
        xy_data.append((time,y))

    return xy_data
