from django.conf.urls import patterns, include, url

from . import views

show_patterns = [
    url(
        r'^$',
        views.ShowListView.as_view(),
        name = 'list',
    ),
    url(
        r'^new/$',
        views.ShowCreateView.as_view(),
        name = 'create',
    ),
    url(
        r'^(?P<slug>[\w-]+)/$',
        views.ShowDetailView.as_view(),
        name = 'detail',
    ),
    # expose show.refresh
    url(
        r'^(?P<slug>[\w-]+)/refresh$',
        views.refresh,
        name = 'refresh',
    ),
]


episode_patterns = [
    url(
        r'^(?P<pk>\d+)/$',
        views.EpisodeDetailView.as_view(),
        name = 'detail',
    ),
]


segment_patterns = [
    url(
        r'new/$',
        views.SegmentCreateView.as_view(),
        name = 'create',
    ),
    url(
        r'^(?P<pk>\d+)/$',
        views.SegmentDetailView.as_view(),
        name = 'detail',
    ),
]

urlpatterns = patterns('',
    url(r'^shows/', include(show_patterns, namespace = 'show')),
    url(r'^episodes/', include(episode_patterns, namespace = 'episode')),
    url(r'^segments/', include(segment_patterns, namespace = 'segment')),
)
