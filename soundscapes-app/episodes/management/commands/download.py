from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

from episodes.handlers.rss import download_episode
from episodes.models import Show

class Command(BaseCommand):
    args = '<show.name, show.name, ...>'
    help = 'Downloads missing .mp3\'s.'

    option_list = BaseCommand.option_list + (
        make_option('--all',
            action = 'store_true',
            dest = 'download_all',
            default = False,
            help = 'Download episodes for all shows'),
        )


    def handle(self, *args, **options):
        show_name_options = Show.objects.values_list('name', flat = True)

        if options['download_all']:
            show_name_choices = show_name_options
        else:
            show_name_choices = args

        for show_name in show_name_choices:
            try:
                show = Show.objects.get(name = show_name)
            except Show.DoesNotExist:
                raise CommandError('Show "{}" does not exist'.format(show_name))

            episodes_missing_mp3s = show.episode_set.filter(mp3 = '')
            for episode in episodes_missing_mp3s:
                self.stdout.write('({}) Downloading: {}'.format(show.name, episode.title))
                episode_mp3 = download_episode(episode.rss_mp3_url)
                episode.mp3 = episode_mp3
                episode.save()
