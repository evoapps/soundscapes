from django.db import models

from manager.models import Episode

class HorizonLine(models.Model):
    """ """
    episode = models.OneToOneField(Episode, related_name = 'horizon_line')

    # A list of heights for this episode, in JSON
    heights = models.TextField()

    # The time interval between height samples
    interval = models.IntegerField()
