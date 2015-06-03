from datetime import datetime
from dateutil import parser

from django.test import TestCase

from model_mommy import mommy

from episodes.models import Show, Episode, Segment

class ModelTest(TestCase):

    def test_episode_manager_creates_new_episodes_with_segment(self):
        show = mommy.make(Show)
        episode_kwargs = {
            'show': show,
            'released': datetime.utcnow(),
            'title': 'My test title',
            'rss': 'http://google.com',
        }
        episode = show.episode_set.create_with_segment(**episode_kwargs)
        self.assertEquals(episode.segment_set.count(), 1)
