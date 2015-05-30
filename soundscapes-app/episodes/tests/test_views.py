from django.core.urlresolvers import reverse
from django.test import TestCase

from model_mommy import mommy

from episodes.models import Episode
from episodes.views import EpisodeListView

class EpisodeViewTest(TestCase):

    def test_episode_list_view_returns_list_of_episodes(self):
        num_episodes = 10
        mommy.make(Episode, _quantity = 10)
        response = self.client.get(reverse('episode_list'))
        episodes = response.context['episode_list']
        self.assertEquals(len(episodes), num_episodes)
