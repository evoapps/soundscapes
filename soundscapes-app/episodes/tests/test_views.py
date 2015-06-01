from unipath import Path

from django.conf import settings
from django.core.files import File
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings

from model_mommy import mommy

from episodes.models import Show, Episode
from episodes.views import (ShowListView, ShowCreateView, ShowDetailView)

class EpisodeViewTest(TestCase):

    def test_show_list_view_returns_list_of_shows(self):
        num_shows = 5
        mommy.make(Show, _quantity = num_shows)
        response = self.client.get(reverse('show_list'))
        shows = response.context['show_list']
        self.assertEquals(len(shows), num_shows)

    def test_show_create_view_creates_new_shows(self):
        show = mommy.prepare(Show)
        post = {'name': show.name, 'rss': show.rss}
        self.client.post(reverse('new_show'), post)
        self.assertEquals(Show.objects.last().name, show.name)
