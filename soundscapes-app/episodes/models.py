from django.db import models

class Show(models.Model):
    name = models.CharField(max_length = 30)

class Episode(models.Model):
    mp3 = models.FileField(max_length = 200, blank = True, null = True)

    show = models.ForeignKey('Show', blank = True, null = True)
    released = models.DateTimeField(blank = True, null = True)
    title = models.CharField(max_length = 80, blank = True, null = True)
