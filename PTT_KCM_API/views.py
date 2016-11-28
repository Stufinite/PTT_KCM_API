from django.shortcuts import render
from django.http import HttpResponse

# import api from view directory
from PTT_KCM_API.api.articles import articles
from PTT_KCM_API.api.ip import ip
from PTT_KCM_API.api.locations import locations
from PTT_KCM_API.api.tfidf import tfidf
from PTT_KCM_API.api.pttJson import pttJson
# Create your views here.

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