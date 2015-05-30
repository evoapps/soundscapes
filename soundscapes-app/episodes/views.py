from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, FormView
from django.shortcuts import render

from .forms import UploadEpisodeForm
from .models import Episode

class EpisodeListView(ListView):
    model = Episode

class EpisodeFormView(FormView):
    form_class = UploadEpisodeForm
    template_name = 'episodes/new_episode.html'
    success_url = reverse_lazy('episode_list')

    def form_valid(self, form):
        form.save()
        return super(EpisodeFormView, self).form_valid(form)

    def form_invalid(self, form):
        print 'invalid form. errors:', form.errors
