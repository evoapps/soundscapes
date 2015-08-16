from django.core.management.base import BaseCommand, CommandError

from episodes.models import Show

class Command(BaseCommand):
    help = 'Retrieve missing RSS entries and save them as Episodes'

    def add_arguments(self, parser):
        parser.add_argument('--show-name', nargs = '+', default = [])
        parser.add_argument('--show-id', nargs = '+', default = [])

    def handle(self, *args, **options):
        shows_to_refresh = []
        shows_to_refresh.extend(Show.objects.filter(name__in = options['show_name']))
        shows_to_refresh.extend(Show.objects.filter(id__in = options['show_id']))

        if not shows_to_refresh:
            shows_to_refresh = Show.objects.all()

        for show in shows_to_refresh:
            self.stdout.write('Refreshing {id}: {name}'.format(id = show.id, name = show.name))
            show.refresh()
