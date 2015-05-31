from dateutil import parser

from django.db import models

from .mp3_handlers import get_mp3_meta_data
from .soundcloud_handlers import (connect_to_soundcloud, search_soundcloud_for,
                                  convert_to_pydatetime)

class ShowManager(models.Manager):

    def create_from_soundcloud_user(self, soundcloud_user, relink = False):
        show_kwargs = {}
        show_kwargs['name'] = soundcloud_user.get('username')
        show_kwargs['soundcloud_id'] = soundcloud_user.get('id')
        new_show, created = self.get_or_create(**show_kwargs)

        if relink:
            new_show.link_to_soundcloud()
            new_show.save()

        return new_show

class Show(models.Model):
    name = models.CharField(unique=True, max_length=30)
    soundcloud_id = models.IntegerField(unique=True, blank=True, null=True)

    objects = ShowManager()

    def link_to_soundcloud(self):
        soundcloud_user = None

        if self.soundcloud_id:
            api_route = '/users/{id}'.format(id = self.soundcloud_id)
            soundcloud_user = search_soundcloud_for(api_route)
        else:
            assert self.name, 'Need name to search with'
            soundcloud_user = search_soundcloud_for('/users', q = self.name)

        # writes over existing show
        if soundcloud_user:
            self.name = soundcloud_user.username
            self.soundcloud_id = soundcloud_user.id

    def pull_episodes_from_soundcloud(self):
        client = connect_to_soundcloud()

        soundcloud_track_ids = self.episode_set.values_list('id', flat = True)

        api_route = '/users/{id}/tracks'.format(id = self.soundcloud_id)
        soundcloud_tracks = client.get(api_route)

        for soundcloud_track in soundcloud_tracks:
            if soundcloud_track.id not in soundcloud_track_ids:
                Episode.objects.create_from_soundcloud_track(soundcloud_track)

class EpisodeManager(models.Manager):

    def create_from_soundcloud_track(self, soundcloud_track, relink = False):
        episode_kwargs = {}

        episode_kwargs['title'] = soundcloud_track.title
        episode_kwargs['soundcloud_id'] = soundcloud_track.id

        soundcloud_user = soundcloud_track.user
        show = Show.objects.create_from_soundcloud_user(soundcloud_user)
        episode_kwargs['show'] = show

        soundcloud_datetime = soundcloud_track.released
        episode_kwargs['released'] = convert_to_pydatetime(soundcloud_datetime)

        new_episode, _ = self.get_or_create(**episode_kwargs)

        if relink:
            new_episode.link_to_soundcloud()
            new_episode.save()

        return new_episode

class Episode(models.Model):
    mp3 = models.FileField(max_length = 200, blank = True, null = True)

    show = models.ForeignKey('Show', blank = True, null = True)
    released = models.DateTimeField(blank = True, null = True)
    title = models.CharField(max_length = 80, blank = True, null = True)

    soundcloud_id = models.IntegerField(blank = True, null = True)

    objects = EpisodeManager()

    def link_to_soundcloud(self):
        client = connect_to_soundcloud()
        soundcloud_track = None

        if self.soundcloud_id:
            api_route = '/tracks/{id}'.format(id = self.soundcloud_id)
            soundcloud_track = search_soundcloud_for(api_route)
        else:
            if not self.title:
                self.title = get_mp3_meta_data(self.mp3.url, 'title')
                assert self.title, 'Need title to search with'
            soundcloud_track = search_soundcloud_for('/tracks', q = self.title)

        # writes over existing track
        if soundcloud_track:

            self.soundcloud_id = soundcloud_track.id
            self.title = soundcloud_track.title

            soundcloud_datetime = soundcloud_track.created_at
            self.released = convert_to_pydatetime(soundcloud_datetime)

            soundcloud_user = soundcloud_track.user
            self.show = Show.objects.create_from_soundcloud_user(
                soundcloud_user, relink = True)
