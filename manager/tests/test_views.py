from unipath import Path

from django.core.urlresolvers import reverse
from django.test import TestCase

from model_mommy import mommy

from manager.models import Show, Episode
from manager.forms import ShowForm
from manager.views import ShowListView, ShowCreateView, ShowDetailView
from manager.views import EpisodeDetailView

class ManagerViewTest(TestCase):

    def test_show_list_view_returns_list_of_shows(self):
        num_shows = 5
        mommy.make(Show, _quantity = num_shows)
        response = self.client.get(reverse('show_list'))
        shows = response.context['show_list']
        self.assertEquals(len(shows), num_shows)

    def test_show_create_view_creates_new_shows(self):
        show = mommy.prepare(Show)
        post = {'name': show.name, 'slug': show.slug, 'rss_url': show.rss_url}
        self.client.post(reverse('show_create'), post)
        self.assertEquals(Show.objects.last().name, show.name)

    def test_show_create_view_renders_show_form(self):
        response = self.client.get(reverse('show_create'))
        show_form = response.context['form']
        self.assertIsInstance(show_form, ShowForm)
