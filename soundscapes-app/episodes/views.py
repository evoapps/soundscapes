from django.views.generic import ListView

from .models import Episode

class EpisodeListView(ListView):
    model = Episode
