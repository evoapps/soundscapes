from django.core.management.base import BaseCommand, CommandError

from episodes.models import Show

class Command(BaseCommand):
    help = 'Refresh each show, download missing episodes, and analyze a segment'

    def add_arguments(self, parser):
        parser.add_argument('--show-name', nargs = '+')

    def handle(self, *args, **options):
        all_show_names = Show.objects.values_list('name', flat = True)
        show_names = options['show_name'] or all_show_names

        for name in show_names:
            try:
                show = Show.objects.get(name = name)
            except Show.DoesNotExist:
                raise CommandError('Show "{}" does not exist'.format(show_name))

            show.refresh()
            for episode in show.episode_set.all():
                episode.download()
                episode.analyze()
