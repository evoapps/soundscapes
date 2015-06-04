from unipath import Path

from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.db import models
from django.utils.text import slugify

from .handlers.rss import (get_entries_in_feed, download_episode,
                           convert_to_pydatetime)

class Show(models.Model):
    name = models.CharField(unique=True, max_length=30)
    rss = models.URLField(unique=True)

    def get_absolute_url(self):
        return '/shows/{pk}/'.format(pk = self.pk)

    def add_new_episodes(self):
        episodes = get_entries_in_feed(self.rss)

        titles = self.episode_set.values_list('title', flat = True)
        new_episodes = filter(lambda x: x['title'] not in titles, episodes)

        for new in new_episodes:
            episode_kwargs = {}
            episode_kwargs['title'] = new['title']
            episode_kwargs['released'] = convert_to_pydatetime(new['published'])
            episode_kwargs['rss_mp3_url'] = new['media_content'][0]['url']

            self.episode_set.create(**episode_kwargs)

class EpisodeManager(models.Manager):
    def create_with_segment(self, *args, **kwargs):
        episode = self.create(**kwargs)
        episode.segment_set.create(start_time = 0.0, end_time = 0.0)
        return episode

class Episode(models.Model):
    show = models.ForeignKey('Show')
    released = models.DateTimeField()
    title = models.CharField(max_length = 80)

    rss_mp3_url = models.URLField(unique = True)
    mp3 = models.FileField(max_length = 200, blank = True)
    duration = models.FloatField(null = True)

    objects = EpisodeManager()

class Segment(models.Model):
    episode = models.ForeignKey('Episode')

    TIME_RESOLUTION = {'max_digits': 10, 'decimal_places': 2}
    start_time = models.DecimalField(**TIME_RESOLUTION)
    end_time = models.DecimalField(**TIME_RESOLUTION)
