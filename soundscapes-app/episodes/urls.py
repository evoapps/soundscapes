from django.conf.urls import patterns, include, url

from .views import EpisodeListView, EpisodeFormView

urlpatterns = patterns('',
    url(r'^list/$', EpisodeListView.as_view(), name = 'episode_list'),
    url(r'^new/$', EpisodeFormView.as_view(), name = 'new_episode'),
)
