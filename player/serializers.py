from rest_framework import serializers

from manager.models import Episode, Segment
from player.models import HorizonLine

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
    class Meta:
        model = HorizonLine
        fields = ('heights', 'interval')


class EpisodeSerializer(serializers.ModelSerializer):
    segments = SegmentSerializer(many = True)
    horizon_line = HorizonLineSerializer()


    class Meta:
        model = Episode
        fields = ('id', 'show', 'released', 'title', 'mp3', 'duration',
                  'segments', 'horizon_line')
