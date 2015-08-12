import json

from rest_framework import serializers

from manager.models import Show, Episode, Segment, Waveform
from player.models import HorizonLine


class ShowSerializer(serializers.ModelSerializer):
    image_url = serializers.CharField(source='get_image_url', read_only=True)
    color_scheme = serializers.SerializerMethodField()

    class Meta:
        model = Show
        fields = ('name', 'image_url', 'color_scheme')

    def get_color_scheme(self, obj):
        """ Try to load the color_scheme as json """
        try:
            return json.loads(obj.color_scheme)
        except ValueError:
            # color_scheme is just a text field so validation
            # is not enforced!
            return obj.color_scheme

class SegmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Segment
        fields = ('start_time', 'end_time')

class WaveformSerializer(serializers.ModelSerializer):
    values = serializers.SerializerMethodField()

    class Meta:
        model = Waveform
        fields = ('interval', 'values')

    def get_values(self, obj):
        try:
            return json.loads(obj.values)
        except ValueError:
            return obj.values

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
    url = serializers.CharField(source='get_mp3_url', read_only=True)
    show = ShowSerializer()
    waveform = WaveformSerializer()

    class Meta:
        model = Episode
        fields = ('id', 'show', 'released', 'title', 'mp3', 'url', 'duration',
                  'segments', 'waveform')
