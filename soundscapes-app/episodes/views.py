from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DetailView
from django.views.decorators.http import require_POST, require_GET

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

@require_GET
def json_episodes(request, pk):
    show = get_object_or_404(Show, pk = pk)
    episodes = show.episode_set.all()
    episodes_json = serializers.serialize('json', episodes)
    return JsonResponse(episodes_json, safe = False)

@require_POST
def download_episode(request, pk):
    episode = get_object_or_404(Episode, pk = pk)
    episode.download()
    episode.save()
    return redirect(episode)
