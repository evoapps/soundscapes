from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, CreateView

from .models import Show, Episode

class ShowListView(ListView):
    model = Show

class ShowCreateView(CreateView):
    model = Show
    success_url = reverse_lazy('show_list')

class EpisodeListView(ListView):
    model = Episode
