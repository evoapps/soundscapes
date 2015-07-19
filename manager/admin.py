from django.contrib import admin

from .models import Show, Episode, Segment


def refresh(modeladmin, request, queryset):
    for show in queryset:
        show.refresh()
refresh.short_description = "Refresh episode feed"

@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    actions = [refresh, ]


def download(modeladmin, request, queryset):
    for episode in queryset:
        episode.download()
download.short_description = "Download the episode"

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_filter = ('show', )
    actions = [download, ]


@admin.register(Segment)
class SegmentAdmin(admin.ModelAdmin):
    pass
