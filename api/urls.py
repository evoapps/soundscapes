from django.conf.urls import patterns, url

from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = patterns('',
    url(
        r'^episodes$',
        views.EpisodeListAPIView.as_view(),
        name = 'json_episode_list',
    ),
    url(
        r'^show/(?P<show>\d+)/episodes$',
        views.EpisodeListAPIView.as_view(),
        name = 'json_episode_list',
    ),
    url(
        r'^episode/(?P<episode>\d+)$',
        views.EpisodeRetrieveAPIView.as_view(),
        name = 'json_episode',
    ),
    url(
        r'^feed$',
        views.EpisodeFeedAPIView.as_view(),
        name = 'json_episode_feed',
    ),
)

router = DefaultRouter()
router.register(r'episodes', views.EpisodeViewSet)
urlpatterns += router.urls
