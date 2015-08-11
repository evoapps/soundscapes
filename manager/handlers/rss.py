from unipath import Path

# RSS handling
import feedparser
import json
from dateutil import parser as dateparser

# Episode downloading
import requests

from django.conf import settings
from django.core.files import File
from django.utils.text import slugify

class RSSHandler(object):
    """ Wrapper around feedparser.parse """
    def __init__(self, rss_url):
        self.feed = feedparser.parse(rss_url)

    def __getitem__(self, key):
        return self.feed[key]

class RSSShowHandler(object):
    """ Interface between an rss url and Show models """
    def __init__(self, rss_url):
        """ Shows are created from the feed """
        rss_handler = RSSHandler(rss_url)
        self.rss_feed = rss_handler['feed']

        self.rss_url = rss_url

    @property
    def name(self):
        return self.rss_feed.get('title', 'Untitled')

    @property
    def slug(self):
        return slugify(self.name)[0:50]

    @property
    def image_url(self):
        # Not sure if it is required that all podcasts have images
        return self.rss_feed['image']['href']

    def show_kwargs(self):
        return {
            # 'rss_url':
            'name': self.name,
            'rss_url': self.rss_url,
            'slug': self.slug,
            'image_url': self.image_url,
        }

class RSSEpisodeHandler(object):
    """ Interface between json RSS entries and Episode models """
    def __init__(self, rss_entry):
        self.rss_entry = rss_entry

    @property
    def released(self):
        """ When the entry was published. Defaults to right now. """
        published = self.rss_entry.get('published', '')
        return dateparser.parse(published)

    @property
    def title(self):
        return self.rss_entry.get('title', 'Untitled')

    @property
    def slug(self):
        return slugify(self.title)[0:50]

    @property
    def mp3_url(self):
        # hack in to the rss_entry get the episode url from the feed host
        return self.rss_entry['media_content'][0]['url']

    @property
    def duration(self):
        """ Duration in seconds """
        # a more accurate way to get the episode duration
        # would be to read the duration from the downloaded mp3.
        durationstr = self.rss_entry.get('itunes_duration', '00:00:00')
        try:
            hours, minutes, seconds = map(int, durationstr.split(':'))
        except ValueError:
            hours = 0
            minutes, seconds = map(int, durationstr.split(':'))
        return (hours*3600) + (minutes*60) + seconds

    @property
    def rss_entry_dump(self):
        """ RSS entry dump """
        # hack! "json.dumps(rss_entry)" chokes on time object
        modified_rss_entry = self.rss_entry.copy()
        modified_rss_entry['published_parsed'] = \
            str(modified_rss_entry['published_parsed'])
        return json.dumps(modified_rss_entry)

    def episode_kwargs(self):
        """ Return RSS fields as kwargs for creating an Episode.

        TODO: parse show from RSS feed
        """
        return {
            # 'show':
            'released': self.released,
            'title': self.title,
            'slug': self.slug,
            'mp3_url': self.mp3_url,
            'duration': self.duration,
            'rss_entry': self.rss_entry_dump,
        }



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
