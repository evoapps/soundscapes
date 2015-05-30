from django.db import models

from .handlers import get_mp3_meta_data, connect_to_soundcloud

class Show(models.Model):
    name = models.CharField(max_length = 30)

class Episode(models.Model):
    mp3 = models.FileField(max_length = 200, blank = True, null = True)

    show = models.ForeignKey('Show', blank = True, null = True)
    released = models.DateTimeField(blank = True, null = True)
    title = models.CharField(max_length = 80, blank = True, null = True)

    soundcloud_track = None
    soundcloud_track_id = models.IntegerField(blank = True, null = True)

    def update(self):
        self.soundcloud_track = self.get_soundcloud_track()

        self.update_show()
        self.update_released()
        self.update_title()
        self.update_soundcloud_track_id()

    def get_soundcloud_track(self):
        if not self.soundcloud_track_id:
            track = self.search_for_soundcloud_track()
        else:
            client = connect_to_soundcloud()
            track = client.get('/tracks', id = self.soundcloud_track_id)
        return track

    def search_for_soundcloud_track(self):
        if not self.title:
            self.title = get_mp3_meta_data(self, key = 'title')

        client = connect_to_soundcloud()
        matching_tracks = client.get('/tracks', q = self.title)
        track = matching_tracks[0]

        return track

    def update_show():
        track = self.soundcloud_track or self.get_soundcloud_track()
        show, _ = Show.objects.get_or_create(name = track.artist)
        self.show = show

    def update_released(soundcloud_track = None):
        track = self.soundcloud_track or self.get_soundcloud_track()
        self.released = track.release_date

    def update_title(soundcloud_track = None):
        track = self.soundcloud_track or self.get_soundcloud_track()
        self.title = track.title

    def update_soundcloud_track_id(soundcloud_track = None):
        track = self.soundcloud_track or self.get_soundcloud_track()
        self.soundcloud_track_id = track.id
