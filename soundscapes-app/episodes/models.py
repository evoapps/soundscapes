from django.db import models

class Episode(models.Model):
    mp3 = models.FileField(blank = True, null = True)
