from django.views.generic import TemplateView

from rest_framework import generics, viewsets
from rest_framework.renderers import JSONRenderer

from manager.models import Show, Episode
from player.serializers import EpisodeSerializer

class FeedView(TemplateView):
    template_name = 'player/index.html'

    def get_context_data(self, **kwargs):
        context_data = super(FeedView, self).get_context_data(**kwargs)
        episodes = Episode.objects.all().order_by('-released')[:10]
        serializer = EpisodeSerializer(episodes, many = True)
        jsoned = JSONRenderer().render(serializer.data)
        context_data['episodes'] = jsoned
        return context_data

class EpisodeViewSet(viewsets.ModelViewSet):
    serializer_class = EpisodeSerializer
    queryset = Episode.objects.all().order_by('-released')
