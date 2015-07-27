import unittest

from django.conf import settings
from django.core.files import File

from manager.handlers import fetch_rss_entries
from manager.handlers import RSSEntryHandler

class HandlerTest(unittest.TestCase):
    def setUp(self):
        self.reply_all_feed = "http://feeds.gimletmedia.com/hearreplyall"

    def test_fetch_rss_entries_limit(self):
        limit = 5
        entries = fetch_rss_entries(self.reply_all_feed, n = limit)
        self.assertLessEqual(len(entries), limit)

    def test_fetch_rss_entries_over_limit(self):
        num_in_feed = len(fetch_rss_entries(self.reply_all_feed))
        over_limit = num_in_feed + 1
        entries = fetch_rss_entries(self.reply_all_feed, n = over_limit)
        self.assertEquals(len(entries), num_in_feed)

class RSSEntryHandlerTest(unittest.TestCase):

    def test_parse_duration(self):

        def _parse_duration(itunes_duration):
            test_rss = {'itunes_duration': itunes_duration}
            handler = RSSEntryHandler(test_rss)
            return handler.duration

        # hours:minutes:seconds format
        self.assertEquals(_parse_duration('00:30:10'), 30 * 60 + 10)

        # minutes:seconds format
        self.assertEquals(_parse_duration('38:36'), 38 * 60 + 36)
