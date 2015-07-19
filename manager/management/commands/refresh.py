from django.core.management.base import BaseCommand, CommandError

from manager.models import Show

class Command(BaseCommand):
    help = 'Retrieve missing RSS entries and save them as Episodes'

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
