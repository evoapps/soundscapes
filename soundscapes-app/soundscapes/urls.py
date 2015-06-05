from django.conf.urls import patterns, include, url
from django.contrib import admin

from episodes import views

urlpatterns = patterns('',
    url(
        r'^shows/$',
        views.ShowListView.as_view(),
        name = 'show_list',
    ),
    url(
        r'^shows/new/$',
        views.ShowCreateView.as_view(),
        name = 'new_show',
    ),
    url(
        r'^shows/(?P<pk>\d+)/$',
        ShowDetailView.as_view(),
        name = 'view_show',
    ),
    url(
        r'^shows/(?P<pk>\d+)/episodes$',
        views.json_episodes,
        name = 'json_episodes',
    ),
)
