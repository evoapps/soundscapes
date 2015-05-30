from django.views.generic import ListView
from django.shortcuts import render

from .models import Episode

class EpisodeListView(ListView):
    model = Episode
