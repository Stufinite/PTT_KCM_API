from django.core.management.base import BaseCommand, CommandError
from PTT_KCM_API.view.pttJson import pttJson

class Command(BaseCommand):
    help = 'use this for activating build_IpTable'
    
    def handle(self, *args, **options):
        p = pttJson()
        p.build_IpTable()
        self.stdout.write(self.style.SUCCESS('build IpTable success!!!'))