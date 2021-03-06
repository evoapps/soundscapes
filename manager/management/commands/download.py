from django.core.management.base import BaseCommand, CommandError

from manager.models import Episode

class Command(BaseCommand):
    help = 'Downloads missing .mp3\'s.'

    def add_arguments(self, parser):
        parser.add_argument('--episode-id', nargs = '+')

    def handle(self, *args, **options):
        all_episodes_ids = Episode.objects.values_list('id', flat = True)
        episode_ids = options['episode_id'] or all_episodes_ids

        for pk in episode_ids:
            try:
                episode = Episode.objects.get(pk = pk)
            except Episode.DoesNotExist:
                raise CommandError('Episode "{}" does not exist'.format(pk))

            episode.download()
