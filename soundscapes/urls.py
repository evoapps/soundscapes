from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

from player.views import FeedView
from player.urls import router

urlpatterns = patterns('',
    url(r'^$', FeedView.as_view(), name = 'feed_view'),
    url(r'^api/', include(router.urls)),
    url(r'^manager/', include('manager.urls')),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
