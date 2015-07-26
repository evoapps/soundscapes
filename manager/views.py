from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DetailView

from .forms import ShowForm, SegmentForm
from .models import Show, Episode, Segment

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
    """ Create new Episodes for any RSS entries not already in the show """
    if request.method == 'POST':
        show = get_object_or_404(Show, slug = slug)
        show.refresh()
        return redirect('show:detail', slug = slug)

class EpisodeDetailView(DetailView):
    model = Episode

    def get_context_data(self, **kwargs):
        context_data = super(EpisodeDetailView, self).get_context_data(**kwargs)
        episode = context_data['episode']
        context_data['show'] = episode.show
        context_data['segments'] = episode.segments.all()
        context_data['segment_form'] = SegmentForm()
        return context_data

class SegmentDetailView(DetailView):
    model = Segment

class SegmentCreateView(CreateView):
    model = Segment
    form_class = SegmentForm
