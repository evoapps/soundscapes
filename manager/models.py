from unipath import Path

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models

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
        return reverse('show:detail', kwargs = {'slug': self.slug})

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

        current_entries = self.episode_set.values_list('rss_entry', flat = True)

        compare_rss_entry_dump = lambda rss_entry: RSSEntryHandler(rss_entry).rss_entry_dump not in current_entries
        new_entries = filter(compare_rss_entry_dump, all_entries)

        for rss_entry in new_entries:
            entry_handler = RSSEntryHandler(rss_entry)
            kwargs = entry_handler.episode_kwargs()
            self.episode_set.create(**kwargs)

    def __str__(self):
        return self.name

class Episode(models.Model):
    """ A RSS entry from a podcast feed """
    show = models.ForeignKey(Show)
    slug = models.SlugField(unique = True)
    rss_entry = models.TextField()

    released = models.DateTimeField()
    title = models.CharField(max_length = 80)

    duration = models.FloatField(null = True)

    mp3_url = models.URLField(unique = True)
    mp3 = models.FileField(max_length = 200, blank = True)

    def get_absolute_url(self):
        return reverse('episode:detail', kwargs = {'pk': self.pk})

    def __str__(self):
        return '{show}: {title}'.format(show = self.show, title = self.title)

    def download(self):
        """ Download the episode

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
