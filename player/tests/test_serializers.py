from django.test import TestCase

from model_mommy import mommy

from manager.models import Episode, Segment
from player.models import HorizonLine
from player.serializers import EpisodeSerializer

class EpisodeSerializerTest(TestCase):

    def test_serialized_episode_includes_segments(self):
        num_segments = 5
        episode = mommy.make(Episode)
        mommy.make(Segment, episode = episode, _quantity = num_segments)
        serializer = EpisodeSerializer(episode)
        self.assertIn('segments', serializer.data.keys())
        segments = serializer.data['segments']
        self.assertEqual(len(segments), num_segments)

    def test_serialized_episode_includes_horizon_line(self):
        episode = mommy.make(Episode)
        mommy.make(HorizonLine, episode = episode)
        serializer = EpisodeSerializer(episode)
        self.assertIn('horizon_line', serializer.data.keys())
