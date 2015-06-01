from dateutil import parser
import feedparser
import urllib

from django.core.files import File

def get_entries_in_feed(rss_url):
    feed = feedparser.parse(rss_url)
    return feed['entries']

def download_episode(downloadable_url):
    path_to_tmp_file, _ = urllib.urlretrieve(downloadable_url)
    tmp_handle = open(path_to_tmp_file, 'rb')
    django_file = File(tmp_handle)
    return django_file

def convert_to_pydatetime(str_datetime):
    return parser.parse(str_datetime)
