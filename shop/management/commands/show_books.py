from django.core.management.base import BaseCommand, CommandError
from shop.models import Book

import pprint


class Command(BaseCommand):
    help = 'Display all available books in the store. To sort books by publish date use:' \
           '\n --sort 1 (for ascending)' \
           '\n --sort 2 (for descending)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--sort',
            dest='sort',
            nargs='?',
            action='store',
            choices=[1, 2],
            default=1,
            type=int,
            help='Sort books by publish date.'
        )

    def handle(self, *args, **options):
        if options['sort'] == 2:
            books = [ obj.as_dict() for obj in Book.objects.all().order_by('publish_date') ]
        else:
            books = [ obj.as_dict() for obj in Book.objects.all().order_by('-publish_date') ]

        # print(books)
        self.stdout.write(self.style.SUCCESS('\nAll available books:'))
        pprint.pprint(books)
