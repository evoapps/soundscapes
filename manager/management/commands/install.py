from django.core.management.base import BaseCommand, CommandError

from manager.models import Show

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('-d', '--download-image', action='store_true', default=False)
        parser.add_argument('-p', '--process-image', action='store_true', default=False)

    def handle(self, *args, **options):
        installed_shows = Show.objects.values_list('rss_url', flat = True)

        show_urls = ['http://feeds.gimletmedia.com/hearstartup',
                     'http://feeds.gimletmedia.com/hearreplyall',
                     'http://feeds.gimletmedia.com/mysteryshow']

        show_urls = filter(lambda x: x not in installed_shows, show_urls)

        for show_url in show_urls:
            Show.objects.create_from_rss_url(show_url)

        shows = Show.objects.all()

        for show in shows:
            show.refresh()

            if options['download_image']:
                show.download_image()

            if options['process_image']:
                if not show.image:
                    show.download_image()

                show.extract_color_scheme()
