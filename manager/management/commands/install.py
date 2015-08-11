from django.core.management.base import BaseCommand, CommandError

from manager.models import Show

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('-d', '--download-image', action='store_true', default=False)

    def handle(self, *args, **options):
        installed_shows = Show.objects.values_list('rss_url', flat = True)

        show_urls = ['http://feeds.gimletmedia.com/hearstartup',
                     'http://feeds.gimletmedia.com/hearreplyall',
                     'http://feeds.gimletmedia.com/mysteryshow']

        show_urls = filter(lambda x: x not in install_shows, show_urls)

        for show_url in show_urls:
            show = Show.objects.create_from_rss_url(show_url)

            if options['download_image']:
                show.download_image()
