from django.test import TestCase

from model_mommy import mommy

from episodes.models import Show, Episode, Segment

class ManagerModelsTest(TestCase):

    def test_show_refresh(self):
        valid_rss_url = "http://feeds.gimletmedia.com/hearstartup"
        show = mommy.make(Show, rss_url = valid_rss_url)
        show.refresh()
        episodes = show.episode_set.all()
        self.assertGreater(len(episodes), 0)
