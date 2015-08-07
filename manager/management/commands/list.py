from django.core.management.base import BaseCommand, CommandError

from manager.models import Episode, Show

class Command(BaseCommand):
    help = 'List Episodes by id'

    def add_arguments(self, parser):
        parser.add_argument('--shows', action = 'store_true', default = False)

    def handle(self, *args, **options):
        if options['shows']:
            for show in Show.objects.all():
                kwargs = {'id': show.id, 'show': show.name}
                self.stdout.write('{id}: {show}'.format(**kwargs))
        else:
            for episode in Episode.objects.all():
                kwargs = {'id': episode.id, 'title': episode.title}
                self.stdout.write('{id}: {title}'.format(**kwargs))
