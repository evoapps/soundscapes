from django.core.management.base import BaseCommand

from episodes.models import Show

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        shows = Show.objects.all()
        for show in shows:
            show.pull_episodes()
