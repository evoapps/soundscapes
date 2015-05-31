from django.core.management.base import BaseCommand

from episodes.models import Show

class Command(BaseCommand):
    args = '<show_name_1, show_name_2, ...>'
    help = 'Search for missing episodes.'

    def handle(self, *args, **kwargs):
        for show_name in args:
            pull_episodes(show_name)

def pull_episodes(show_name):
    show = Show.objects.get(name = show_name)
    show.pull_episodes_from_soundcloud()
