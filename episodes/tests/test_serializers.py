import json

from django.test import TestCase

from model_mommy import mommy

from episodes.models import Show, Episode, Segment
from episodes.serializers import EpisodeSerializer, ShowSerializer

class EpisodeSerializerTest(TestCase):

    def test_serialized_episode_includes_show(self):
        show = mommy.make(Show)
        episode = mommy.make(Episode, show = show)
        serializer = EpisodeSerializer(episode)
        serialized_show = serializer.data['show']
        self.assertIn('name', serialized_show.keys())
        self.assertEquals(serialized_show['name'], show.name)

    def test_serialized_episode_includes_segments(self):
        num_segments = 5
        episode = mommy.make(Episode)
        mommy.make(Segment, episode = episode, _quantity = num_segments)
        serializer = EpisodeSerializer(episode)
        self.assertIn('segments', serializer.data.keys())
        segments = serializer.data['segments']
        self.assertEqual(len(segments), num_segments)

    def test_serialized_episode_includes_mp3_url(self):
        episode = mommy.make(Episode, _fill_optional = 'mp3')
        serializer = EpisodeSerializer(episode)
        self.assertIn('mp3', serializer.data.keys())
        self.assertEquals(serializer.data['mp3'], episode.mp3.url)

    def test_serialized_show_correctly_parses_color_scheme(self):
        color_scheme = ['rgb(0,0,0)', 'rgb(1,1,1)']
        color_scheme_dump = json.dumps(color_scheme)
        show = mommy.make(Show, color_scheme = color_scheme_dump)
        serializer = ShowSerializer(show)
        self.assertEquals(serializer.data['color_scheme'], color_scheme)
