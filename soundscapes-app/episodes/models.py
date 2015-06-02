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
            episode_kwargs['rss'] = new['media_content'][0]['url']

            self.episode_set.create(**episode_kwargs)

class EpisodeFileStorage(FileSystemStorage):
    def get_available_name(self, name):
        """ Overwrites files with same name """
        return name

class Episode(models.Model):
    show = models.ForeignKey('Show')
    released = models.DateTimeField()
    title = models.CharField(max_length = 80)

    rss = models.URLField(unique=True)
    mp3 = models.FileField(max_length = 200, blank = True, null = True,
                           storage = EpisodeFileStorage())

    def download_mp3(self):
        mp3_dst_kwargs = {
            'show': slugify(self.name),
            'episode': slugify(self.title),
        }
        mp3_dst = '{show}-{episode}.mp3'.format(**mp3_dst_kwargs)
        episode_kwargs['mp3'] = download_episode(self.rss, mp3_dst)
