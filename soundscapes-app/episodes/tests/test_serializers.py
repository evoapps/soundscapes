
from django.test import TestCase

from model_mommy import mommy

from episodes.models import Episode
from episodes.serializers import EpisodeSerializer

class SerializerTest(TestCase):
    def test_serialized_episode_has_episode_url(self):
        episode = mommy.make(Episode)
        serializer = EpisodeSerializer(episode)
        data = serializer.data
        self.assertIn('url', data.keys())
