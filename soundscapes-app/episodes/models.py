from dateutil import parser as dateparser
import json
import pydub
from unipath import Path

from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.db import models
from django.utils.text import slugify

from .handlers import fetch_rss_entries, download_episode, get_audio_duration

class Show(models.Model):
    name = models.CharField(unique = True, max_length = 30)
    rss_url = models.URLField(unique = True)

    def get_absolute_url(self):
        return '/shows/{pk}/'.format(pk = self.pk)

    def refresh(self):
        """ Create episodes from new RSS entries """
        print 'refreshing'
        all_entries = fetch_rss_entries(self.rss_url)
        current_entries = self.episode_set.values_list('rss_entry', flat = True)
        new_entries = filter(lambda entry: entry not in current_entries,
                             all_entries)
        for rss_entry in new_entries:
            Episode.objects.create_from_rss_entry(rss_entry, show = self)

class EpisodeManager(models.Manager):
    def create_from_rss_entry(self, rss_entry, show):
        """ Create an episode from an RSS entry

        Episodes are created from parsed JSON only, meaning episodes
        are created without mp3's or mp3 analysis (e.g., duration).
        """
        kwargs = {
            'show': show,
            'released': dateparser.parse(rss_entry['published']),
            'title': rss_entry['title'],
            'rss_mp3_url': rss_entry['media_content'][0]['url'],
        }

        # hack! json.dumps chokes on time object
        modified_rss_entry = rss_entry.copy()
        modified_rss_entry['published_parsed'] = \
            str(modified_rss_entry['published_parsed'])
        rss_entry_dumps = json.dumps(modified_rss_entry)
        kwargs['rss_entry'] = rss_entry_dumps

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

    def get_absolute_url(self):
        return '/episodes/{pk}/'.format(pk = self.pk)

    def download(self):
        """ Download the episode file and analyze its duration

        Episodes are only downloaded if the mp3 FileField is empty. Analyzing
        the episode duration here is not necessary but the file is already
        open.
        """
        if not self.mp3:
            mp3 = download_episode(self.rss_mp3_url)
            self.mp3 = mp3
            self.duration = get_audio_duration(mp3)
            self.save()

    def analyze(self):
        """ Create an initial segment spanning the episode

        Segments are only created if none yet exist.
        """
        if self.segment_set.count() == 0:
            self.segment_set.create(start_time = 0.0, end_time = self.duration)

class Segment(models.Model):
    episode = models.ForeignKey('Episode')

    TIME_RESOLUTION = {'max_digits': 10, 'decimal_places': 2}
    start_time = models.DecimalField(**TIME_RESOLUTION)
    end_time = models.DecimalField(**TIME_RESOLUTION)
