from django.core import serializers
from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DetailView
from django.views.decorators.http import require_POST, require_GET

from .forms import ShowForm
from .models import Show

class ShowListView(ListView):
    model = Show

class ShowCreateView(CreateView):
    model = Show
    form_class = ShowForm

class ShowDetailView(DetailView):
    model = Show

@require_POST
def refresh_show(request, pk):
    show = get_object_or_404(Show, pk = pk)
    show.add_new_episodes()
    return redirect(show)

@require_GET
def get_episodes_as_json(request, pk):
    show = get_object_or_404(Show, pk = pk)
    episodes = show.episode_set.all()
    episodes_json = serializers.serialize('json', episodes)
    return JsonResponse(episodes_json, safe = False)
