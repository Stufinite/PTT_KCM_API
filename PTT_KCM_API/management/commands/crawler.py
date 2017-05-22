from django.core.management.base import BaseCommand, CommandError
from PttWebCrawler import *

class Command(BaseCommand):
    help = 'use this to download ptt articles json'

    def add_arguments(self, parser):
        parser.add_argument('board', type=str)
        parser.add_argument('start', type=int)
        parser.add_argument('end', type=int)

    def handle(self, *args, **options):
        PttWebCrawler(options['board'], True , start=options['start'], end=options['end'])
        self.stdout.write(self.style.SUCCESS('down ptt articles success!!!'))