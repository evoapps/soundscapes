from unipath import Path

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models

from .handlers.downloads import download_file
from .handlers.rss import RSSHandler, RSSShowHandler, RSSEpisodeHandler
from .handlers.image import extract_color_scheme, serialize_color_scheme
from .handlers.waveform import get_waveform

# Decimal field kwargs for moments and segments
TIME_RESOLUTION = {'max_digits': 10, 'decimal_places': 2}

class ShowManager(models.Manager):
    def create_from_rss_url(self, rss_url, **kwargs):
        rss_show = RSSShowHandler(rss_url)
        kwargs.update(rss_show.show_kwargs())
        return self.create(**kwargs)

class Show(models.Model):
    """ A collection of Episodes, plugged in to an RSS podcast feed """
    name = models.CharField(unique = True, max_length = 30)
    slug = models.SlugField(unique = True)
    rss_url = models.URLField(unique = True)

    image_url = models.URLField()
    image = models.ImageField(blank = True)

    color_scheme = models.TextField()

    objects = ShowManager()

    def get_absolute_url(self):
        return reverse('show:detail', kwargs = {'slug': self.slug})

    def get_image_url(self):
        if self.image:
            return self.image.url
        else:
            return None

    def download_image(self):
        """ Download the image

        Images are downloaded if the image FileFiled is empty or if the
        file doesn't exist on the server.
        """
        if not self.image or not Path(self.image.path).exists():
            self.image = download_file(self.image_url)
            self.save()

    def extract_color_scheme(self):
        if not self.image:
            raise AssertionError('Logo is not available')

        color_scheme = extract_color_scheme(self.image.path)
        self.color_scheme = serialize_color_scheme(color_scheme)
        self.save()

    def refresh(self, max = 10):
        """ Create episodes from new RSS entries

        Evaluates uniqueness based on "rss_entry" field.

        max: int, number of entries to retrieve. A max number of entries
             are fetched before determining uniquess. Passing None will
             fetch all episodes.

        TODO: add "revert" as an optional argument.
        TODO: hash the rss_entry instead of comparing full json
        """
        all_entries = RSSHandler(self.rss_url)['entries'][0:max]

        current_entries = self.episode_set.values_list('rss_entry', flat = True)

        def compare_rss_entry_dump(rss_entry):
            return RSSEpisodeHandler(rss_entry).rss_entry_dump not in current_entries
        new_entries = filter(compare_rss_entry_dump, all_entries)

        for rss_entry in new_entries:
            self.episode_set.create_from_rss_entry(rss_entry)

    def __str__(self):
        return self.name

class EpisodeManager(models.Manager):
    def create_from_rss_entry(self, rss_entry, **kwargs):
        entry_handler = RSSEpisodeHandler(rss_entry)
        kwargs.update(entry_handler.episode_kwargs())
        return self.create(**kwargs)

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

    objects = EpisodeManager()

    def get_absolute_url(self):
        return reverse('episode:detail', kwargs = {'pk': self.pk})

    def get_mp3_url(self):
        if self.mp3:
            return self.mp3.url
        else:
            return None

    def __str__(self):
        return '{show}: {title}'.format(show = self.show, title = self.title)

    def download(self):
        """ Download the episode

        Episodes are downloaded if the mp3 FileField is empty or if the file
        doesn't exist on the server.

        TODO: use case for "overwrite" as an optional argument?
        """
        if not self.mp3 or not Path(self.mp3.path).exists():
            self.mp3 = download_file(self.mp3_url)
            self.save()

    def analyze(self, reset):
        if not self.mp3:
            raise AssertionError('No episode file. Download episode first.')

        try:
            has_waveform = (self.waveform is not None)
        except Waveform.DoesNotExist:
            has_waveform = False

        if has_waveform and reset:
            self.waveform.delete()
            has_waveform = False

        if not has_waveform:
            interval = 5 # seconds
            values = get_waveform(self.mp3.path, interval = interval)
            Waveform.objects.create(episode = self, interval = interval, values = values)

class Segment(models.Model):
    """ A section of an Episode

    TODO: validate time fields in clean method
    """
    episode = models.ForeignKey(Episode, related_name = 'segments')

    start_time = models.DecimalField(**TIME_RESOLUTION)
    end_time = models.DecimalField(**TIME_RESOLUTION)

class Waveform(models.Model):
    episode = models.OneToOneField(Episode, primary_key = True)
    interval = models.IntegerField()
    values = models.TextField()

    def delete(self, *args, **kwargs):
        analysis_txt = Path(self.episode.mp3.path).name + '.csv'
        analysis_txt = Path(settings.ANALYSES_DIR, analysis_txt)
        if analysis_txt.exists():
            analysis_txt.remove()
        return super(Waveform, self).delete(*args, **kwargs)

class Tag(models.Model):
    name = models.CharField(max_length = 150)
    segment = models.ForeignKey(Segment, related_name = 'tags',
                                related_query_name = 'tag')
