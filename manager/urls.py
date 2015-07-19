
from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

from . import views

urlpatterns = patterns('',
    url(
        r'^$',
        views.ShowListView.as_view(),
        name = 'show_list',
    ),
    url(
        r'^new/$',
        views.ShowCreateView.as_view(),
        name = 'show_create',
    ),
    url(
        r'^(?P<slug>[\w-]+)/$',
        views.ShowDetailView.as_view(),
        name = 'show_detail',
    ),
    url(
        r'^(?P<show_slug>[\w-]+)/(?P<episode_slug>[\w-]+)/$',
        views.EpisodeDetailView.as_view(),
        name = 'episode_detail',
    ),
)
