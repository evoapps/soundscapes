from dateutil import parser

from django.db import models

from .mp3_handlers import get_mp3_meta_data
from .soundcloud_handlers import connect_to_soundcloud

class Show(models.Model):
    name = models.CharField(unique = True, max_length = 30)
    soundcloud_id = models.IntegerField(blank = True, null = True)

    def link_to_soundcloud(self):
        client = connect_to_soundcloud()
        soundcloud_user = None

        if self.soundcloud_id:
            api_route = '/users/{id}'.format(id = self.soundcloud_id)
            soundcloud_user = client.get(api_route)
        else:
            assert self.name, 'Need name to search with'
            matching_users = client.get('/users', q = self.name)
            for match in matching_users:
                gimlet_in_website = hasattr(match, 'website') and \
                                    match.website.find('gimlet') > 0
                # add other match conditions here

                if gimlet_in_website:
                    soundcloud_user = match
                    break

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
                released = _convert_to_pydatetime(soundcloud_track.created_at)

                episode = Episode(
                    soundcloud_id = soundcloud_track.id,
                    title = soundcloud_track.title,
                    show = self,
                    released = released,
                )
                episode.full_clean()
                episode.save()


class Episode(models.Model):
    mp3 = models.FileField(max_length = 200, blank = True, null = True)

    show = models.ForeignKey('Show', blank = True, null = True)
    released = models.DateTimeField(blank = True, null = True)
    title = models.CharField(max_length = 80, blank = True, null = True)

    soundcloud_id = models.IntegerField(blank = True, null = True)

    def link_to_soundcloud(self):
        client = connect_to_soundcloud()
        soundcloud_track = None

        if self.soundcloud_id:
            api_route = '/tracks/{id}'.format(id = self.soundcloud_id)
            soundcloud_track = client.get(api_route)
        else:
            if not self.title:
                self.title = get_mp3_meta_data(self.mp3.url, 'title')
            assert self.title, 'Need title to search with'
            matching_tracks = client.get('/tracks', q = self.title)
            for match in matching_tracks:
                gimlet_in_tag_list = hasattr(match, 'tag_list') and \
                                     match.tag_list.find('gimlet') > 0
                # add other match conditions here

                if gimlet_in_tag_list:
                    soundcloud_track = match
                    break

        # writes over existing track
        if soundcloud_track:
            self.soundcloud_id = soundcloud_track.id
            self.title = soundcloud_track.title

            soundcloud_datetime = soundcloud_track.created_at
            self.released = _convert_to_pydatetime(soundcloud_datetime)

            soundcloud_user = soundcloud_track.user
            soundcloud_username = soundcloud_user['username']
            soundcloud_user_id = soundcloud_user['id']

            show, created = Show.objects.get_or_create(
                name = soundcloud_username,
                soundcloud_id = soundcloud_user_id)

            if created:
                show.link_to_soundcloud()
                show.save()

            self.show = show

def _convert_to_pydatetime(soundcloud_datetime):
    return parser.parse(soundcloud_datetime)
