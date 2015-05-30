from django.conf.urls import patterns, include, url

from .views import EpisodeListView

urlpatterns = patterns('',
    url(r'^list/$', EpisodeListView.as_view(), name = 'episode_list'),
)
