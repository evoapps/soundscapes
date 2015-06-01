from django.conf.urls import patterns, include, url
from django.contrib import admin

from episodes.views import (ShowListView, ShowCreateView, ShowDetailView)

urlpatterns = patterns('',
    url(r'^shows/$', ShowListView.as_view(), name = 'show_list'),
    url(r'^shows/new/$', ShowCreateView.as_view(), name = 'new_show'),
    url(r'^shows/(?P<pk>\d+)/$', ShowDetailView.as_view(), name = 'view_show'),
)
