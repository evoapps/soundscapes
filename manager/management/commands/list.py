from django.core.management.base import BaseCommand, CommandError

from manager.models import Episode

class Command(BaseCommand):
    help = 'List Episodes by id'

    def handle(self, *args, **options):
        for episode in Episode.objects.all():
            kwargs = {'id': episode.id, 'title': episode.title}
            self.stdout.write('{id}: {title}'.format(**kwargs))
