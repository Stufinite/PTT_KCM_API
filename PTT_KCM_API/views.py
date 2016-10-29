from django.shortcuts import render
from django.http import HttpResponse

# import api from view directory
from PTT_KCM_API.api.articles import articles, pttJson
from PTT_KCM_API.api.ip import ip
from PTT_KCM_API.api.locations import locations
from PTT_KCM_API.api.pttJson import pttJson
# Create your views here.

def build_IpTable(request):
	p = pttJson()
	p.build_IpTable()
	return HttpResponse("Build IpTable!!!")