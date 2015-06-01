from dateutil import parser
import feedparser
import requests
from unipath import Path

from django.conf import settings
from django.core.files import File

def get_entries_in_feed(rss_url):
    feed = feedparser.parse(rss_url)
    return feed['entries']

def download_episode(downloadable_url, dst_stem):
    expected_dst = Path(settings.MEDIA_ROOT, dst_stem)

    # only download if necessary
    if not expected_dst.exists():
        response = requests.get(downloadable_url)
        with open(expected_dst, 'wb') as dst_handle:
            dst_handle.write(response.content)

    tmp_handle = open(expected_dst, 'rb')
    django_file = File(tmp_handle)
    return django_file

def convert_to_pydatetime(str_datetime):
    return parser.parse(str_datetime)
