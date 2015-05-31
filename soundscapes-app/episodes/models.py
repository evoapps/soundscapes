from datetime.datetime import strpftime
SOUNDCLOUD_DATETIME_FORMT = "%Y/%m/%d %H:%M:%S +0000"

from django.db import models

from .handlers import get_mp3_meta_data, connect_to_soundcloud

class Show(models.Model):
    name = models.CharField(unique = True, max_length = 30)
    soundcloud_id = models.IntegerField(blank = True, null = True)

    def link_to_soundcloud(self):
        client = connect_to_soundcloud()

        soundcloud_show = None

        matching_shows = client.get('/users', q = self.name)
        for match in matching_shows:
            try:
                if match.website.find('gimletmedia') > 0:
                    soundcloud_show = match
                    break
            except AttributeError:
                # e.g., match.website is None
                pass

        if soundcloud_show:
            self.soundcloud_id = soundcloud_show.id

class Episode(models.Model):
    mp3 = models.FileField(max_length = 200, blank = True, null = True)

    show = models.ForeignKey('Show', blank = True, null = True)
    released = models.DateTimeField(blank = True, null = True)
    title = models.CharField(max_length = 80, blank = True, null = True)

    soundcloud_id = models.IntegerField(blank = True, null = True)

    def link_to_soundcloud(self):
        client = connect_to_soundcloud()

        if not self.title:
            self.title = get_mp3_meta_data(self.mp3.url, key = 'title')

        soundcloud_track = None

        matching_tracks = client.get('/tracks', q = self.title)
        for match in matching_tracks:
            try:
                if match.website.find('gimletmedia') > 0:
                    soundcloud_track = match
                    break
            except AttributeError:
                # e.g., match.website is None
                pass

        if soundcloud_track:
            self.soundcloud_id = soundcloud_track.id
            self.title = soundcloud_track.title

            soundcloud_datetime = soundcloud_track.created_at
            py_datetime = strpftime(soundcloud_datetime,
                                    SOUNDCLOUD_DATETIME_FORMAT)
            self.released = py_datetime

            show_name = soundcloud_track.artist
            show, created = Show.objects.get_or_create(name = show_name)

            if created:
                show.link_to_soundcloud()
                show.save()

            self.show = show
