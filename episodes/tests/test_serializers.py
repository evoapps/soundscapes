
from django.test import TestCase

from model_mommy import mommy

from episodes.models import Episode, Moment, Segment
from episodes.serializers import EpisodeSerializer

class SerializerTest(TestCase):
    def test_serialized_episode_has_episode_url(self):
        episode = mommy.make(Episode)
        serializer = EpisodeSerializer(episode)
        data = serializer.data
        self.assertIn('url', data.keys())
        self.assertEqual(data['url'], episode.get_absolute_url())

    def test_serialized_episode_has_moment_data(self):
        num_moments = 10
        episode = mommy.make(Episode)
        moments = mommy.make(Moment, episode = episode, _quantity = num_moments)
        segment = mommy.make(Segment, episode = episode, moments = moments)

        serializer = EpisodeSerializer(episode)
        data = serializer.data

        self.assertIn('segments', data.keys())
        segment_data = data['segments'][0]

        self.assertIn('moments', segment_data.keys())
        segment_moment_data = segment_data['moments'][0]
        self.assertIn('time', segment_moment_data)
        self.assertIn('value', segment_moment_data)
