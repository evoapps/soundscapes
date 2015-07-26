from rest_framework import serializers

from manager.models import Episode, Segment
from player.models import HorizonLine, SegmentBubble

class SegmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Segment
        fields = ('start_time', 'end_time')

class HorizonLineSerializer(serializers.ModelSerializer):
    """
    var horizon_line_generator = d3.svg.line()
      .y(function (height, i) { return horizon_line.interval; })

    d3.select("path")
      .data(horizon_line.heights)
      .append("path")
      .attr("d", horizon_line_generator)
    """
    segments = SegmentSerializer(many = True)

    class Meta:
        model = HorizonLine
        fields = ('heights', 'interval', 'segments')


class SegmentBubbleSerializer(serializers.ModelSerializer):

    class Meta:
        model = SegmentBubble
        fields = ('size', )


class EpisodeSerializer(serializers.ModelSerializer):
    horizon_line = HorizonLineSerializer()
    segment_bubbles = SegmentBubbleSerializer(many = True)

    class Meta:
        model = Episode
        fields = ('id', 'show', 'released', 'title', 'mp3', 'duration',
                  'horizon_line', 'segment_bubbles')
