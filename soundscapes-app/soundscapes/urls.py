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
        views.ShowDetailView.as_view(),
        name = 'view_show',
    ),
    url(
        r'^api/episodes$',
        views.EpisodeListAPIView.as_view(),
        name = 'json_episodes',
    ),
    url(
        r'^api/episodes/(?P<show>\d+)$',
        views.EpisodeListAPIView.as_view(),
        name = 'json_episodes',
    ),
    url(
        r'^episodes/(?P<pk>\d+)/$',
        views.EpisodeDetailView.as_view(),
        name = 'view_episode',
    ),
    url(
        r'^episodes/(?P<pk>\d+)/download$',
        views.download_episode,
        name = 'download_episode',
    ),
)
