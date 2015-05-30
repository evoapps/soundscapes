from unipath import Path

from django.core.files import File
from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings

from episodes.forms import UploadEpisodeForm

TEST_MEDIA_ROOT = Path(settings.MEDIA_ROOT + '-test')

@override_settings(MEDIA_ROOT = TEST_MEDIA_ROOT, MEDIA_URL = '/media-test/')
class EpisodeFormTest(TestCase):

    def tearDown(self):
        TEST_MEDIA_ROOT.rmtree()
        super(EpisodeFormTest, self).tearDown()

    def test_uploading_new_episode_strips_meta_data_from_mp3(self):
        path_to_new_episode = Path(settings.BASE_DIR, 'episodes/tests/fixtures',
                                   'reply-all-26.mp3')

        with open(path_to_new_episode, 'rb') as episode_handle:
            episode_file = File(episode_handle)
            form = UploadEpisodeForm(files = {'mp3': episode_file})
            self.assertTrue(form.is_valid())
            episode = form.save()

        self.assertEquals(episode.show.name, 'Reply All')
