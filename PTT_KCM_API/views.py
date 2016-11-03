from django.shortcuts import render
from django.http import HttpResponse

# import api from view directory
from PTT_KCM_API.api.articles import articles
from PTT_KCM_API.api.ip import ip
from PTT_KCM_API.api.locations import locations
from PTT_KCM_API.api.pttJson import pttJson
# Create your views here.

def build_IpTable(request):
	p = pttJson()
	p.build_IpTable()
	return HttpResponse("Build IpTable!!!")

def build_IpTable_with_IpList1(request):
	p = pttJson()
	p.build_IpTable_with_IpList('1_1500.txt')
	return HttpResponse("Build IpTable with List 1_1500!!!")

def build_IpTable_with_IpList2(request):
	p = pttJson()
	p.build_IpTable_with_IpList('1500_4000.txt')
	return HttpResponse("Build IpTable with List 1500_4000!!!")

def build_IpTable_with_IpList3(request):
	p = pttJson()
	p.build_IpTable_with_IpList('4000_4133.txt')
	return HttpResponse("Build IpTable with List 4000_4133 !!!")