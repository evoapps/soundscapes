from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

from manager import views

urlpatterns = patterns('',
    url(
        r'^$',
        TemplateView.as_view(template_name = 'index.html'),
    ),
    url(
        r'^feed/$',
        TemplateView.as_view(template_name = 'episodes/episode_feed.html'),
        name = 'episode_feed',
    ),
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
        r'^episodes/(?P<pk>\d+)/$',
        views.EpisodeDetailView.as_view(),
        name = 'view_episode',
    ),
    url(r'^api/', include('api.urls')),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
