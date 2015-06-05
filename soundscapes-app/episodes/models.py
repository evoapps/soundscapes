from unipath import Path

from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.db import models
from django.utils.text import slugify

from .handlers.rss import (get_entries_in_feed, download_episode,
                           convert_to_pydatetime)

class Show(models.Model):
    name = models.CharField(unique = True, max_length = 30)
    rss_url = models.URLField(unique = True)

    def get_absolute_url(self):
        return '/shows/{pk}/'.format(pk = self.pk)

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
