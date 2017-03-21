from django.core.management.base import BaseCommand, CommandError
from PTT_KCM_API.view.pttJson import pttJson

class Command(BaseCommand):
    help = 'use this for activating build_IpTable'
    
    def handle(self, *args, **options):
    	from project.settings_database import uri
    	from pymongo import MongoClient
    	from PTT_KCM_API.view.dictionary.postokenizer import PosTokenizer
    	from PTT_KCM_API.trigger_cache.trigger_cache import trigger_cache
    	import json, pyprind, pymongo
    	client = MongoClient(uri)
    	db = client['ptt']
    	articlesCollect = db['articles']
    	IndexCollect = db['invertedIndex']
    	articlesCollect.remove({})
    	IndexCollect.remove({})
    	db['ip'].remove({})
    	db['locations'].remove({})

    	key = dict()
    	articleList = []
    	p = pttJson()

    	f = json.load(open(p.filePath, 'r', encoding='utf-8-sig'))

    	articlesCollect.insert(f['articles'])

    	bar = pyprind.ProgBar( articlesCollect.find().count())
    	for i in articlesCollect.find().batch_size(500):
    		# pymongo Cursor with timeout if time of query data exceed 10 minutes.
    		# so setting batch_size will fetch amount of document from mongo 
    		# in per query.
    		# But there is no universal "right" batch_size
    		# You should test with different values and see what is the appropriate value for your use case i.e. how many documents can you process in a 10 minute window.
    		# http://stackoverflow.com/questions/24199729/pymongo-errors-cursornotfound-cursor-id-not-valid-at-server

    		bar.update()
    		if i.get('article_id', None) == None:
    			continue

    		objectID = i['_id']
    		
    		uniqueTerm = set(PosTokenizer('' if i.get('article_title', '')==None else i.get('article_title', ''), ['n']))
    		uniqueTerm = uniqueTerm.union(PosTokenizer('' if i.get('content', '')==None else i.get('content', ''), ['n']))
    		for k in uniqueTerm:
    			key.setdefault(k, []).append(objectID)


    	IndexList = tuple({'ObjectID':v, 'issue':k} for k, v in key.items())
    	IndexCollect.insert(IndexList)
    	IndexCollect.create_index([("issue", pymongo.HASHED)])

    	self.stdout.write(self.style.SUCCESS('insert Articles success!!!'))