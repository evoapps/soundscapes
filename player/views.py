from django.views.generic import TemplateView

from rest_framework import generics, viewsets
from rest_framework.renderers import JSONRenderer

from manager.models import Show, Episode
from .serializers import EpisodeSerializer

class FeedView(generics.ListAPIView):
    template_name = 'player/index.html'
    serializer_class = EpisodeSerializer
    queryset = Episode.objects.all().order_by('-released')

    #
    #
    # def get_context_data(self, **kwargs):
    #     context_data = super(FeedView, self).get_context_data(**kwargs)
    #
    #     queryset = Episode.objects.all().order_by('-released')
    #     context_data['episodes'] = EpisodeSerializer(queryset, many = True).data
    #
    #     return context_data

class EpisodeViewSet(viewsets.ModelViewSet):
    serializer_class = EpisodeSerializer
    queryset = Episode.objects.all().order_by('-released')
