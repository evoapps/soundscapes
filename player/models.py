from django.db import models

from manager.models import Episode

class HorizonLine(models.Model):
    """ """
    episode = models.ForeignKey(Episode)

    # A list of heights for this episode, in JSON
    heights = models.TextField()

    # The time interval between height samples
    interval = models.IntegerField()

class SegmentBubble(models.Model):
    episode = models.ForeignKey(Episode)

    size = models.IntegerField()
