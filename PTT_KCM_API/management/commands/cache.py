from django.core.management.base import BaseCommand, CommandError
from PTT_KCM_API.view.pttJson import pttJson
import sys

class Command(BaseCommand):
    help = 'use this for activating build_IpTable'
    
    def handle(self, *args, **options):
    	import requests
    	with open('PTT_KCM_API/management/commands/issue.txt', 'r', encoding='utf-8') as f:
    		for i in f:
    			i = i.encode(sys.stdin.encoding, "replace").decode(sys.stdin.encoding)
    			i = i.strip()
    			print(i)
    			re = requests.get('http://127.0.0.1:8000/PTT_KCM_API/api/locations/',{'issue':i})
