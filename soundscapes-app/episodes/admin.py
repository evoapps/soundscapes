from django.contrib import admin

from .models import Show, Episode, Segment


def refresh(modeladmin, request, queryset):
    for show in queryset:
        show.refresh()
refresh.short_description = "Refresh episode feed"

@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    actions = [refresh, ]

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_filter = ('show', )

@admin.register(Segment)
class SegmentAdmin(admin.ModelAdmin):
    pass
