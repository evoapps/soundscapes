from django.db import model

from manager.models import Episode

class HorizonLine(model.Model):
    """ """
    episode = models.ForeignKey(Episode)

    # A list of heights for this episode, in JSON
    heights = models.TextField()

    # The time interval between height samples
    interval = models.IntegerField()

class SegmentBubble(model.Model):
    episode = models.ForeignKey(Episode)

    size = models.IntegerField()
