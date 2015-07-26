from django.db import models

from manager.models import Episode

class HorizonLine(models.Model):
    """ """
    episode = models.OneToOneField(Episode, related_name = 'horizon_line')

    # A list of heights for this episode, in JSON
    heights = models.TextField()

    # The time interval between height samples
    interval = models.IntegerField()

    def segments(self):
        return self.episode.segments

class SegmentBubble(models.Model):
    episode = models.ForeignKey(Episode, related_name = 'segment_bubbles')

    size = models.IntegerField()
