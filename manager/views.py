from django.views.generic import ListView, CreateView, DetailView

from .forms import ShowForm
from .models import Show, Episode

class ShowListView(ListView):
    model = Show

class ShowCreateView(CreateView):
    model = Show
    form_class = ShowForm

class ShowDetailView(DetailView):
    model = Show

class EpisodeDetailView(DetailView):
    model = Episode
