from django.views.generic import ListView, FormView
from django.shortcuts import render

from .forms import UploadEpisodeForm
from .models import Episode

class EpisodeListView(ListView):
    model = Episode

class EpisodeFormView(FormView):
    form_class = UploadEpisodeForm
    template_name = 'episodes/new_episode.html'
