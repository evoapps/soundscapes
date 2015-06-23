from django.contrib import admin

from .models import Show, Episode, Segment

@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    pass

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    pass

@admin.register(Segment)
class SegmentAdmin(admin.ModelAdmin):
    pass
