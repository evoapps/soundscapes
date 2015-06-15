
from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Show, Episode, Segment

class SegmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Segment

class EpisodeSerializer(serializers.ModelSerializer):
    segments = SegmentSerializer(many = True)
    url = serializers.URLField(source = 'get_absolute_url')

    class Meta:
        model = Episode
        fields = ('id', 'show', 'released', 'title', 'mp3', 'segments',
                  'url')
        depth = 1
