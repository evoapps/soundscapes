from dateutil import parser as dateparser
from unipath import Path

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models

from .handlers import fetch_rss_entries, dump_rss_entry
from .handlers import download_episode, get_audio_duration

class Show(models.Model):
    """ A collection of Episodes, plugged in to an RSS podcast feed """
    name = models.CharField(unique = True, max_length = 30)
    rss_url = models.URLField(unique = True)

    def get_absolute_url(self):
        # reverse(...) should work. Weird import somewhere.
        return '/shows/{pk}/'.format(pk = self.pk)

    def refresh(self, max = 10):
        """ Create episodes from new RSS entries

        Evaluates uniqueness based on "rss_entry" field.

        max: int, number of entries to retrieve. A max number of entries
             are fetched before determining uniquess. Passing None will
             fetch all episodes.

        TODO: add "revert" as an optional argument.
        """
        all_entries = fetch_rss_entries(self.rss_url, n = max)
        current_entries = self.episode_set.values_list('rss_entry', flat = True)
        new_entries = filter(lambda e: dump_rss_entry(e) not in current_entries,
                             all_entries)
        for rss_entry in new_entries:
            Episode.objects.create_from_rss_entry(rss_entry, show = self)

class EpisodeManager(models.Manager):
    def create_from_rss_entry(self, rss_entry, show):
        """ Create an episode from an RSS entry

        Episodes are created from parsed JSON only, meaning episodes
        are created without mp3s or mp3 analysis (e.g., duration).

        TODO: implement a better way to deserialize a JSON RSS entry.
        """
        kwargs = {
            'show': show,
            'released': dateparser.parse(rss_entry['published']),
            'title': rss_entry['title'],
            'rss_mp3_url': rss_entry['media_content'][0]['url'],
            'rss_entry': dump_rss_entry(rss_entry),
        }
        return self.create(**kwargs)

class Episode(models.Model):
    """ A RSS entry from a podcast feed """
    show = models.ForeignKey(Show)
    rss_entry = models.TextField()

    released = models.DateTimeField()
    title = models.CharField(max_length = 80)

    rss_mp3_url = models.URLField(unique = True)

    # mp3 and analyses require downloading the episode
    mp3 = models.FileField(max_length = 200, blank = True)
    duration = models.FloatField(null = True)

    objects = EpisodeManager()

    def get_absolute_url(self):
        # reverse(...) should work. Weird import somewhere.
        return '/episodes/{pk}/'.format(pk = self.pk)

    def download(self):
        """ Download the episode file and analyze its duration

        Episodes are only downloaded if the mp3 FileField is empty. Analyzing
        the episode duration here is not necessary but the file is already
        open.

        TODO: use case for "overwrite" as an optional argument?

        URGENT: add boolean argument "analyze" that defaults to True,
                and use it to trigger self.analyze. Duration should be
                bundled with self.analyze.
        """
        if not self.mp3:
            mp3 = download_episode(self.rss_mp3_url)
            self.mp3 = mp3
            self.duration = get_audio_duration(mp3)
            self.save()

    def analyze(self):
        """ Create an initial segment spanning the episode

        Segments are only created if none yet exist.

        TODO: add "reset" optional argument
        """
        if self.segments.count() == 0:
            self.segments.create(start_time = 0.0, end_time = self.duration)

class Segment(models.Model):
    """ A section of an Episode

    TODO: validate time fields in clean method
    """
    episode = models.ForeignKey(Episode, related_name = 'segments')

    TIME_RESOLUTION = {'max_digits': 10, 'decimal_places': 2}
    start_time = models.DecimalField(**TIME_RESOLUTION)
    end_time = models.DecimalField(**TIME_RESOLUTION)
