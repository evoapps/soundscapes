from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView

from .models import Show

class ShowListView(ListView):
    model = Show

class ShowCreateView(CreateView):
    model = Show

class ShowDetailView(DetailView):
    model = Show
