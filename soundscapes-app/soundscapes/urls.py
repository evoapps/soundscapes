from django.conf.urls import patterns, include, url
from django.contrib import admin

import episodes.views

urlpatterns = patterns('',
    url(
        r'^shows/$',
        episodes.views.ShowListView.as_view(),
        name = 'show_list',
    ),
    url(
        r'^shows/new/$',
        episodes.views.ShowCreateView.as_view(),
        name = 'new_show',
    ),
    url(
        r'^shows/(?P<pk>\d+)/$',
        episodes.views.ShowDetailView.as_view(),
        name = 'view_show',
    ),
    url(
        r'^shows/(?P<pk>\d+)/episodes$',
        episodes.views.json_episodes,
        name = 'json_episodes',
    ),
)
