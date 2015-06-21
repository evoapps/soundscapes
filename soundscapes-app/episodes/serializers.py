
from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Show, Episode, Moment, Segment

class MomentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Moment

class SegmentSerializer(serializers.ModelSerializer):
    moments = MomentSerializer(many = True)

    class Meta:
        model = Segment
        fields = ('id', 'start_time', 'end_time', 'moments')

class EpisodeSerializer(serializers.ModelSerializer):
    segments = SegmentSerializer(many = True)
    url = serializers.URLField(source = 'get_absolute_url')

    class Meta:
        model = Episode
        fields = ('id', 'show', 'released', 'title', 'mp3', 'duration',
                  'segments', 'moments', 'url')
        depth = 1
