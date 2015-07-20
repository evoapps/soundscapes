from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
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

    def get_context_data(self, **kwargs):
        context_data = super(ShowDetailView, self).get_context_data(**kwargs)
        show = context_data['show']
        context_data['episode_list'] = show.episode_set.all().order_by('-released')
        return context_data

def refresh(request, slug):
    if request.method == 'POST':
        show = get_object_or_404(Show, slug = slug)
        show.refresh()
        return redirect('show_detail', slug = slug)

class EpisodeDetailView(DetailView):
    model = Episode
    slug_url_kwarg = 'episode_slug'
