from dateutil import parser as dateutil_parser
import feedparser
import json
import pydub
from unipath import Path

from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.db import models
from django.utils.text import slugify

from .handlers import download_episode

class Show(models.Model):
    name = models.CharField(unique = True, max_length = 30)
    rss_url = models.URLField(unique = True)

    def get_absolute_url(self):
        return '/shows/{pk}/'.format(pk = self.pk)

    def refresh(self):
        """ Fetch RSS entries """
        feed = feedparser.parse(self.rss_url)
        all_entries = feed['entries']
        episode_entries = self.episode_set.values_list('rss_entry', flat = True)
        new_entries = filter(lambda entry: entry not in episode_entries,
                             all_entries)
        for rss_entry in new_entries:
            Episode.objects.create_from_rss_entry(rss_entry, show = self)

class EpisodeManager(models.Manager):
    def create_from_rss_entry(self, rss_entry, show):

        # hack!
        rss_entry_content = rss_entry.copy()
        rss_entry_content['published_parsed'] = str(rss_entry_content['published_parsed'])

        kwargs = {
            'show': show,
            'rss_entry': json.dumps(rss_entry_content, skipkeys = True),
            'released': dateutil_parser.parse(rss_entry['published']),
            'title': rss_entry['title'],
            'rss_mp3_url': rss_entry['media_content'][0]['url'],
        }
        return self.create(**kwargs)

class Episode(models.Model):
    show = models.ForeignKey('Show')
    rss_entry = models.TextField()

    released = models.DateTimeField()
    title = models.CharField(max_length = 80)

    rss_mp3_url = models.URLField(unique = True)

    mp3 = models.FileField(max_length = 200, blank = True)
    duration = models.FloatField(null = True)

    objects = EpisodeManager()

    def download(self):
        if not self.mp3:
            mp3 = download_episode(self.rss_mp3_url)
            self.mp3 = mp3

            audio_segment = pydub.AudioSegment.from_mp3(mp3)
            self.duration = audio_segment.duration_seconds

            self.save()

    def analyze(self):
        if self.segment_set.count() == 0:
            self.segment_set.create(start_time = 0.0, end_time = self.duration)

class Segment(models.Model):
    episode = models.ForeignKey('Episode')

    TIME_RESOLUTION = {'max_digits': 10, 'decimal_places': 2}
    start_time = models.DecimalField(**TIME_RESOLUTION)
    end_time = models.DecimalField(**TIME_RESOLUTION)
