
from rest_framework import serializers

from .models import Show, Episode, Segment

class SegmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Segment

class EpisodeSerializer(serializers.ModelSerializer):
    segment_set = SegmentSerializer(many = True)

    class Meta:
        model = Episode
        fields = ('id', 'show', 'released', 'title', 'mp3', 'segment_set')
        depth = 1
