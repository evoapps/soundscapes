from django.conf.urls import patterns, include, url
from django.contrib import admin

from episodes.views import (ShowListView, ShowCreateView, ShowDetailView,
                            refresh_show, get_episodes_as_json)

urlpatterns = patterns('',
    url(r'^shows/$', ShowListView.as_view(), name = 'show_list'),
    url(r'^shows/new/$', ShowCreateView.as_view(), name = 'new_show'),
    url(r'^shows/(?P<pk>\d+)/$', ShowDetailView.as_view(), name = 'view_show'),
    url(r'^shows/(?P<pk>\d+)/refresh$', refresh_show, name = 'refresh_show'),
    url(r'^shows/(?P<pk>\d+)/episodes$', get_episodes_as_json, name = 'get_episodes_as_json'),
)
