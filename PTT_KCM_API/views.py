from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# import api from view directory
from PTT_KCM_API.view.articles import articles
from PTT_KCM_API.view.ip import ip
from PTT_KCM_API.view.locations import locations
from PTT_KCM_API.view.tfidf import tfidf
from PTT_KCM_API.view.pttJson import pttJson
# Create your views here.
def buildArticle2DB(request):
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

	f = json.load(open(p.filePath, 'r', encoding='utf8'))

	articlesCollect.insert(f['articles'])

	bar = pyprind.ProgBar( articlesCollect.find().count())
	for i in articlesCollect.find():
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

	trigger_cache()
	return JsonResponse({"status":"success"})

def build_IpTable(request):
	p = pttJson()
	p.build_IpTable()
	return HttpResponse("Build IpTable!!!")

def build_IpTable_with_IpList(request):
	if request.GET:
		file = request.GET['file']
		apiKey = request.GET['apiKey']
		p = pttJson()
		p.build_IpTable_with_IpList(file, apiKey)
	return HttpResponse("Build IpTable with List {} and key {}!!!".format(file, apiKey))

def putIntoDB(request):
	if request.GET:
		jsonfile = request.GET['file']
		p = pttJson()
		p.putIntoDB(jsonfile)
	return HttpResponse("putIntoDB {} finish!!".format(jsonfile))