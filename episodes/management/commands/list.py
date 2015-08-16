from django.core.management.base import BaseCommand, CommandError

from episodes.models import Episode, Show

class Command(BaseCommand):
    help = 'List Episodes by id'

    def add_arguments(self, parser):
        parser.add_argument('--list-shows', action = 'store_true', default = False)
        parser.add_argument('--show-name', nargs = '+', default = [])
        parser.add_argument('--show-id', nargs = '+', default = [])

    def handle(self, *args, **options):
        if options['list_shows']:
            for show in Show.objects.all():
                kwargs = {'id': show.id, 'show': show.name}
                self.stdout.write('{id}: {show}'.format(**kwargs))
        else:
            shows = []
            shows.extend(Show.objects.filter(name__in = options['show_name']))
            shows.extend(Show.objects.filter(id__in = options['show_id']))

            if not shows:
                shows = Show.objects.all()

            episodes = Episode.objects.filter(show__in = shows)
            for episode in episodes:
                kwargs = {'id': episode.id, 'show': episode.show, 'title': episode.title}
                self.stdout.write('{id}: ({show}) {title}'.format(**kwargs))
