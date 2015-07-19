import json
from unipath import Path

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.six import BytesIO

from model_mommy import mommy
from rest_framework.parsers import JSONParser

from manager.models import Show, Episode
from manager.serializers import EpisodeSerializer
from manager.views import (ShowListView, ShowCreateView, ShowDetailView)

class EpisodeViewTest(TestCase):

    def _parse_response_json(self, response):
        """ Given a response from self.client, parse the JSON data """
        response_json = response._container[0]
        response_stream = BytesIO(response_json)
        return JSONParser().parse(response_stream)

    def test_show_list_view_returns_list_of_shows(self):
        num_shows = 5
        mommy.make(Show, _quantity = num_shows)
        response = self.client.get(reverse('show_list'))
        shows = response.context['show_list']
        self.assertEquals(len(shows), num_shows)

    def test_show_create_view_creates_new_shows(self):
        show = mommy.prepare(Show)
        post = {'name': show.name, 'rss_url': show.rss_url}
        self.client.post(reverse('new_show'), post)
        self.assertEquals(Show.objects.last().name, show.name)

    def test_get_episodes_as_json(self):
        show = mommy.make(Show)
        mommy.make(Episode, show = show, _quantity = 5)
        episodes = show.episode_set.all()
        expected_episodes_serializer = EpisodeSerializer(episodes, many = True)
        expected_data = expected_episodes_serializer.data

        url = reverse('json_episode_list')
        response = self.client.get(url)
        response_data = self._parse_response_json(response)

        self.assertEqual(expected_data, response_data)

    def test_get_related_episodes_as_json(self):
        """ Only return the episodes of a particular show """
        show = mommy.make(Show)
        mommy.make(Episode, show = show, _quantity = 5)

        other_show = mommy.make(Show)
        mommy.make(Episode, show = other_show, _quantity = 5)

        selected_episodes = show.episode_set.all()
        selected_episodes_serializer = EpisodeSerializer(selected_episodes,
                                                         many = True)
        selected_data = selected_episodes_serializer.data

        url = reverse('json_episode_list', kwargs = {'show': show.pk})
        response = self.client.get(url)
        response_data = self._parse_response_json(response)

        self.assertEqual(selected_data, response_data)

    def test_get_single_episode_as_json(self):
        """ Episode detail view requires returning a single episode """
        episode = mommy.make(Episode, _quantity = 10)[5]
        episode_serializer = EpisodeSerializer(episode)
        episode_data = episode_serializer.data

        url = reverse('json_episode', kwargs = {'episode': episode.pk})
        response = self.client.get(url)
        response_data = self._parse_response_json(response)

        self.assertEqual(episode_data, response_data)
