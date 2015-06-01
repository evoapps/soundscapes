from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DetailView
from django.views.decorators.http import require_POST

from .models import Show

class ShowListView(ListView):
    model = Show

class ShowCreateView(CreateView):
    model = Show

class ShowDetailView(DetailView):
    model = Show

@require_POST
def refresh_show(request, pk):
    show = get_object_or_404(Show, pk = pk)
    show.add_new_episodes()
    return redirect(show)
