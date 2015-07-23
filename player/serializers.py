from rest_framework import serializers

from manager.models import Show, Episode, Segment

class SegmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Segment
        fields = ('id', 'start_time', 'end_time')

class EpisodeSerializer(serializers.ModelSerializer):
    segments = SegmentSerializer(many = True)
    url = serializers.URLField(source = 'get_absolute_url')

    class Meta:
        model = Episode
        fields = ('id', 'show', 'released', 'title', 'mp3', 'duration',
                  'segments', 'url')
        depth = 1
