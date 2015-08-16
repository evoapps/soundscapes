from unipath import Path

from django.core.urlresolvers import reverse
from django.test import TestCase

from model_mommy import mommy

from episodes.models import Show, Episode, Segment
from episodes.forms import ShowForm, SegmentForm

class ShowViewsTest(TestCase):

    def setUp(self):
        self.valid_rss_url = 'http://feeds.gimletmedia.com/hearstartup'

    def test_show_list_view_returns_list_of_shows(self):
        num_shows = 5
        mommy.make(Show, _quantity = num_shows)
        response = self.client.get(reverse('show:list'))
        shows = response.context['show_list']
        self.assertEquals(len(shows), num_shows)

    def test_show_create_view_creates_new_shows(self):
        post = {'rss_url': self.valid_rss_url}
        self.client.post(reverse('show:create'), post)
        self.assertEquals(Show.objects.last().name, 'StartUp Podcast')

    def test_show_create_view_renders_show_form(self):
        response = self.client.get(reverse('show:create'))
        show_form = response.context['form']
        self.assertIsInstance(show_form, ShowForm)

    def test_show_detail_view_adds_show_episodes_to_context(self):
        num_episodes = 5
        show = mommy.make(Show)
        mommy.make(Episode, show = show, _quantity = num_episodes)
        response = self.client.get(show.get_absolute_url())
        self.assertIn('episode_list', response.context.keys())
        self.assertEquals(len(response.context['episode_list']), num_episodes)

    def test_show_refresh_view_fetches_new_episodes(self):
        show = mommy.make(Show, rss_url = self.valid_rss_url)
        response = self.client.post(reverse('show:refresh', kwargs = {'slug': show.slug}))
        self.assertEquals(response.status_code, 302)
        episodes = show.episode_set.all()
        self.assertGreater(len(episodes), 0)


class EpisodeDetailViewTest(TestCase):

    def test_adds_show_to_context(self):
        episode = mommy.make(Episode)
        response = self.client.get(episode.get_absolute_url())
        self.assertIn('show', response.context.keys())
        self.assertEquals(response.context['show'], episode.show)

    def test_adds_segments_to_context(self):
        num_segments = 5
        episode = mommy.make(Episode)
        mommy.make(Segment, episode = episode, _quantity = num_segments)
        response = self.client.get(episode.get_absolute_url())
        self.assertIn('segments', response.context.keys())
        self.assertEquals(len(response.context['segments']), num_segments)

    def test_adds_segment_form_to_context(self):
        episode = mommy.make(Episode)
        response = self.client.get(episode.get_absolute_url())
        self.assertIn('segment_form', response.context.keys())
        self.assertIsInstance(response.context['segment_form'], SegmentForm)
