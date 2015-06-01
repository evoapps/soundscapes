from django.conf.urls import patterns, include, url
from django.contrib import admin

from episodes.views import ShowListView, ShowCreateView, EpisodeListView

urlpatterns = patterns('',
    url(r'^shows/$', ShowListView.as_view(), name = 'show_list'),
    url(r'^shows/new/$', ShowCreateView.as_view(), name = 'new_show'),
    url(r'^episodes/$', EpisodeListView.as_view(), name = 'episode_list'),
)
