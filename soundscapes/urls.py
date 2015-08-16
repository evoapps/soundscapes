from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

from rest_framework.routers import DefaultRouter

from episodes import views

# API router
router = DefaultRouter()
router.register(r'episodes', views.EpisodeViewSet)

show_patterns = [
    url(r'^$', views.ShowListView.as_view(), name='list'),
    url(r'^new/$', views.ShowCreateView.as_view(), name='create'),
    url(r'^(?P<slug>[\w-]+)/$', views.ShowDetailView.as_view(), name='detail'),
    # expose show.refresh
    url(r'^(?P<slug>[\w-]+)/refresh$', views.refresh, name='refresh'),
]

episode_patterns = [
    url(r'^(?P<pk>\d+)/$', views.EpisodeDetailView.as_view(), name='detail'),
]

segment_patterns = [
    url(r'new/$', views.SegmentCreateView.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$', views.SegmentDetailView.as_view(),name='detail'),
]

urlpatterns = patterns('',
    url(r'^$', views.FeedView.as_view(), name = 'feed_view'),
    url(r'^api/', include(router.urls)),

    url(r'^shows/', include(show_patterns, namespace = 'show')),
    url(r'^episodes/', include(episode_patterns, namespace = 'episode')),
    url(r'^segments/', include(segment_patterns, namespace = 'segment')),

    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
