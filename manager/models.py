from dateutil import parser as dateparser
from unipath import Path

from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils.text import slugify

from .handlers import fetch_rss_entries
from .handlers import RSSEntryHandler
from .handlers import download_episode

# Decimal field kwargs for moments and segments
TIME_RESOLUTION = {'max_digits': 10, 'decimal_places': 2}

class Show(models.Model):
    """ A collection of Episodes, plugged in to an RSS podcast feed """
    name = models.CharField(unique = True, max_length = 30)
    slug = models.SlugField(unique = True)
    rss_url = models.URLField(unique = True)

    def get_absolute_url(self):
        return reverse('show_detail', kwargs = {'slug': self.slug})

    def refresh(self, max = 10):
        """ Create episodes from new RSS entries

        Evaluates uniqueness based on "rss_entry" field.

        max: int, number of entries to retrieve. A max number of entries
             are fetched before determining uniquess. Passing None will
             fetch all episodes.

        TODO: add "revert" as an optional argument.
        TODO: hash the rss_entry instead of comparing full json
        """
        all_entries = fetch_rss_entries(self.rss_url, n = max)
        all_entries_json = []
        for rss_entry in all_entries:
            rss_handler = RSSEntryHandler(rss_entry)
            all_entries_json.append(rss_handler.rss_entry)

        current_entries = self.episode_set.values_list('rss_entry', flat = True)

        new_entries = filter(lambda e: e not in current_entries,
                             all_entries_json)

        for rss_entry in new_entries:
            Episode.objects.create_from_rss_entry(rss_entry, show = self)

    def __str__(self):
        return self.name

class EpisodeManager(models.Manager):
    def create_from_rss_entry(self, rss_entry, show):
        """ Create an Episode from an RSS entry """
        entry_handler = RSSEntryHandler(rss_entry)
        kwargs = entry_handler.episode_kwargs()

        # RSSEntryHandler does not process the show from the entry
        kwargs['show'] = show

        return self.create(**kwargs)

class Episode(models.Model):
    """ A RSS entry from a podcast feed """
    show = models.ForeignKey(Show)
    slug = models.SlugField(unique = True)
    rss_entry = models.TextField()

    released = models.DateTimeField()
    title = models.CharField(max_length = 80)

    rss_mp3_url = models.URLField(unique = True)

    # mp3 and analyses require downloading the episode
    mp3 = models.FileField(max_length = 200, blank = True)
    duration = models.FloatField(null = True)

    objects = EpisodeManager()

    def get_absolute_url(self):
        slug_kwargs = {'show_slug': self.show.slug, 'episode_slug': self.slug}
        return reverse('episode_detail', kwargs = slug_kwargs)

    def __str__(self):
        return '{show}: {title}'.format(show = self.show, title = self.title)

    def download(self):
        """ Download the episode file

        Episodes are downloaded if the mp3 FileField is empty or if the file
        doesn't exist on the server.

        TODO: use case for "overwrite" as an optional argument?
        """
        if not self.mp3 or not Path(self.mp3.path).exists():
            self.mp3 = download_episode(self.mp3_url)
            self.save()

class Segment(models.Model):
    """ A section of an Episode

    TODO: validate time fields in clean method
    """
    episode = models.ForeignKey(Episode, related_name = 'segments')

    start_time = models.DecimalField(**TIME_RESOLUTION)
    end_time = models.DecimalField(**TIME_RESOLUTION)

class Tag(models.Model):
    name = models.CharField(max_length = 150)
    segment = models.ForeignKey(Segment, related_name = 'tags',
                                related_query_name = 'tag')
