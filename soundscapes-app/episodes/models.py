from django.db import models

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
            mp3_url = new['media_content'][0]['url']
            episode_kwargs['mp3'] = download_episode(mp3_url)
            episode_kwargs['title'] = new['title']
            episode_kwargs['released'] = convert_to_pydatetime(new['published'])
            self.episode_set.create(**episode_kwargs)

class Episode(models.Model):
    show = models.ForeignKey('Show')
    released = models.DateTimeField()
    title = models.CharField(max_length = 80)

    mp3 = models.FileField(max_length = 200, blank = True, null = True)
