import unittest

from django.conf import settings
from django.core.files import File

from manager import handlers

class RSSEpisodeHandlerTest(unittest.TestCase):
    def test_parse_duration(self):
        def _parse_duration(itunes_duration):
            test_rss = {'itunes_duration': itunes_duration}
            handler = handlers.RSSEpisodeHandler(test_rss)
            return handler.duration

        # hours:minutes:seconds format
        self.assertEquals(_parse_duration('00:30:10'), 30 * 60 + 10)

        # minutes:seconds format
        self.assertEquals(_parse_duration('38:36'), 38 * 60 + 36)

    def test_trim_slug(self):
        very_long_title = 'a' * 100
        handler = handlers.RSSEpisodeHandler({'title': very_long_title})
        self.assertLessEqual(len(handler.slug), 50)
