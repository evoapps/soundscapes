from django.db import models

from .handlers.rss import (get_entries_in_feed, download_episode,
                           convert_to_pydatetime)

class Show(models.Model):
    name = models.CharField(unique=True, max_length=30)
    rss = models.URLField(unique=True)

    def pull_episodes(self):
        episodes = get_entries_in_feed(self.rss)

        titles = self.episode_set.values_list('title', flat = True)
        new_episodes = filter(lambda x: x['title'] not in titles, episodes)

        for new in new_episodes:
            episode_kwargs = {}
            episode_kwargs['title'] = new['title']
            episode_kwargs['mp3'] = download_episode(new['media_content'][0]['url'])
            episode_kwargs['released'] = convert_to_pydatetime(new['published'])
            self.episode_set.create(**episode_kwargs)

class Episode(models.Model):
    mp3 = models.FileField(max_length = 200, blank = True, null = True)

    show = models.ForeignKey('Show', blank = True, null = True)
    released = models.DateTimeField(blank = True, null = True)
    title = models.CharField(max_length = 80, blank = True, null = True)
