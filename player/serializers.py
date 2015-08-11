import json

from rest_framework import serializers

from manager.models import Show, Episode, Segment
from player.models import HorizonLine

class JSONSerializerField(serializers.Field):
    """ Serializer for JSONField -- required to make field writable"""
    def to_internal_value(self, data):
        return data
    def to_representation(self, value):
        print 'to_representation', value
        return value

class ShowSerializer(serializers.ModelSerializer):
    image_url = serializers.CharField(source='get_image_url', read_only=True)
    color_scheme = serializers.SerializerMethodField()

    class Meta:
        model = Show
        fields = ('name', 'image_url', 'color_scheme')

    def get_color_scheme(self, obj):
        try:
            return json.loads(obj.color_scheme)
        except ValueError:
            return obj.color_scheme

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
    url = serializers.CharField(source='get_mp3_url', read_only=True)
    show = ShowSerializer()

    class Meta:
        model = Episode
        fields = ('id', 'show', 'released', 'title', 'mp3', 'url', 'duration',
                  'segments', 'horizon_line')
