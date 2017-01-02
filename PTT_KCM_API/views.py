from django.shortcuts import render
from django.http import HttpResponse

# import api from view directory
from PTT_KCM_API.view.articles import articles
from PTT_KCM_API.view.ip import ip
from PTT_KCM_API.view.locations import locations
from PTT_KCM_API.view.tfidf import tfidf
from PTT_KCM_API.view.pttJson import pttJson
# Create your views here.
def buildArticle2DB(request, uri=None):
	from pymongo import MongoClient
	from PTT_KCM_API.view.dictionary.postokenizer import PosTokenizer
	import json
	client = MongoClient(uri)
	db = client['ptt']
	collect = db['articles']
	f = json.load(open('ptt-web-crawler/HatePolitics-2-4.json', 'r', encoding='utf8'))
	for i in f['articles']:
		key = set(PosTokenizer(i['article_title'], ['n']))
		key = key.union(PosTokenizer(i['content'], ['n']))
		for k in key:
			collect.update({'issue':k}, {'$push':{'articleID':i['article_id']}}, upsert=True)

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