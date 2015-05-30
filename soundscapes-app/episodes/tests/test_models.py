from unipath import Path

from django.core.files import File
from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings

from model_mommy import mommy

from episodes.models import Show, Episode

TEST_MEDIA_ROOT = Path(settings.MEDIA_ROOT + '-test')

@override_settings(MEDIA_ROOT = TEST_MEDIA_ROOT, MEDIA_URL = '/media-test/')
class EpisodeModelsTest(TestCase):

    def tearDown(self):
        TEST_MEDIA_ROOT.rmtree()
        super(EpisodeModelsTest, self).tearDown()

    def test_look_up_episode_info(self):
        path_to_new_episode = Path(settings.BASE_DIR, 'episodes/tests/fixtures',
                                   'reply-all-26.mp3')

        with open(path_to_new_episode, 'rb') as episode_handle:
            episode_file = File(episode_handle)
            episode = Episode(mp3 = episode_file)
            episode.save()

        episode.update()
        self.assertEquals(episode.show.name, 'Reply All')
