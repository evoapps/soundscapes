from django.test import TestCase

from model_mommy import mommy

from manager.models import Episode, Segment
from player.models import HorizonLine, SegmentBubble
from player.serializers import EpisodeSerializer

class EpisodeSerializerTest(TestCase):

    def test_serialized_episode_includes_horizon_line(self):
        num_segments = 5
        episode = mommy.make(Episode)
        mommy.make(HorizonLine, episode = episode)
        serializer = EpisodeSerializer(episode)
        self.assertIn('horizon_line', serializer.data.keys())
