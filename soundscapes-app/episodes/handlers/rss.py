from dateutil import parser
import feedparser
import tempfile
import requests
from unipath import Path

from django.conf import settings
from django.core.files import File
from django.utils.text import slugify

def refresh_show(show):
    rss = feedparser.parse(show.rss)
    entries = rss['entries']


    titles = self.episode_set.values_list('title', flat = True)
    new_episodes = filter(lambda x: x['title'] not in titles, episodes)

    for new in new_episodes:
        episode_kwargs = {}
        episode_kwargs['title'] = new['title']
        episode_kwargs['released'] = convert_to_pydatetime(new['published'])
        episode_kwargs['rss_mp3_url'] = new['media_content'][0]['url']

        self.episode_set.create(**episode_kwargs)

def get_entries_in_feed(rss_url):
    feed = feedparser.parse(rss_url)
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

def convert_to_pydatetime(str_datetime):
    return parser.parse(str_datetime)
