from django.core.management.base import BaseCommand

from episodes.models import Show

class Command(BaseCommand):
    args = '<show_name_1, show_name_2, ...>'
    help = 'Populate the database with some shows. Idempotent.'

    def handle(self, *args, **kwargs):
        for show_name in args:
            add_show(show_name)

def add_show(show_name):
    show, created = Show.objects.get_or_create(name = show_name)

    if created:
        show.link_to_soundcloud()
        show.save()

    return show
