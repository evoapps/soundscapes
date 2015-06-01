from unipath import Path

from django.conf import settings
from django.core.files import File
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings

from model_mommy import mommy

from episodes.models import Episode
from episodes.views import EpisodeListView

TEST_MEDIA_ROOT = Path(settings.MEDIA_ROOT + '-test')

@override_settings(MEDIA_ROOT = TEST_MEDIA_ROOT, MEDIA_URL = '/media-test/')
class EpisodeViewTest(TestCase):

    def tearDown(self):
        TEST_MEDIA_ROOT.rmtree()
        super(EpisodeViewTest, self).tearDown()

    def test_episode_list_view_returns_list_of_episodes(self):
        num_episodes = 10
        mommy.make(Episode, _quantity = 10)
        response = self.client.get(reverse('episode_list'))
        episodes = response.context['episode_list']
        self.assertEquals(len(episodes), num_episodes)
