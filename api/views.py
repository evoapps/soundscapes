from rest_framework import generics, viewsets

from episodes.models import Show, Episode
from .serializers import EpisodeSerializer

class EpisodeViewSet(viewsets.ModelViewSet):
    serializer_class = EpisodeSerializer
    queryset = Episode.objects.all().order_by('-released')

class EpisodeListAPIView(generics.ListAPIView):
    """ Serialize a list of episodes """
    serializer_class = EpisodeSerializer

    def get_queryset(self):
        queryset = Episode.objects.all().order_by('-released')

        show = self.kwargs.get('show', None)
        if show is not None:
            queryset = queryset.filter(show__pk = show)

        return queryset

class EpisodeFeedAPIView(generics.ListAPIView):
    """ Serialize a list of episodes """
    serializer_class = EpisodeSerializer
    queryset = Episode.objects.all().order_by('-released')

class EpisodeRetrieveAPIView(generics.RetrieveAPIView):
    """ Serialize individual episodes

    TODO: combine EpisodeListAPI and EpisodeRetrieveAPI into GenericAPIView
    """
    queryset = Episode.objects.all()
    serializer_class = EpisodeSerializer
    lookup_url_kwarg = 'episode'
