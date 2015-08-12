from django.core.management.base import BaseCommand, CommandError

from manager.models import Episode

class Command(BaseCommand):
    help = 'Process .mp3 and create a segment'

    def add_arguments(self, parser):
        parser.add_argument('--episode-id', nargs = '+')
        parser.add_argument('-r', '--reset', action='store_true', default=False)

    def handle(self, *args, **options):
        all_episodes_ids = Episode.objects.values_list('id', flat = True)
        episode_ids = options['episode_id'] or all_episodes_ids

        for pk in episode_ids:
            try:
                episode = Episode.objects.get(pk = pk)
            except Episode.DoesNotExist:
                raise CommandError('Episode "{}" does not exist'.format(pk))

            episode.analyze(reset = options['reset'])
