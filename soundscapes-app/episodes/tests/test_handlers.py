import random
from unipath import Path
import unittest

from django.conf import settings
from django.core.files import File

from episodes.handlers import fetch_rss_entries
from episodes.handlers import get_audio_duration
from episodes.handlers import get_audio_features

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

    def test_get_episode_duration(self):
        to_episode = Path(settings.BASE_DIR, 'ftests/fixtures/reply-all-26.mp3')
        episode_file = File(open(to_episode, 'rb'))
        duration = get_audio_duration(episode_file)
        self.assertIsInstance(duration, float)
        self.assertGreater(duration, 0)

        episode_file.close()

    def test_get_audio_features(self):
        to_episode = Path(settings.BASE_DIR, 'ftests/fixtures/reply-all-26.mp3')
        episode_file = File(open(to_episode, 'rb'))
        xy_data = get_audio_features(episode_file)
        self.assertGreater(len(xy_data), 0)
        sample_x, sample_y = xy_data[0]
        self.assertIsInstance(sample_y, float)

        episode_file.close()
