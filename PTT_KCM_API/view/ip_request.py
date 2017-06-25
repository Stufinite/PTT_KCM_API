# -*- coding: utf-8 -*-
import requests
import sys
from bs4 import BeautifulSoup
from PTT_KCM_API.models import IP,Ip2location

def build_map(ipList, result):
	''' Create map instance.

	dbip: ip-location json return from dbip api.
	
	if clause: if key name (eq:台南) doesn't exist, then create dict with that key name and calculate score and attendee.
	'''
	for ip, score in ipList:
		if score == 0:
			continue
		try:
			ipresult = IP.objects.get(ip = ip)
			countryName = ipresult.countryName
			stateProv = ipresult.stateProv
			city = ipresult.city

		except Exception as e:
			dbip = getIP2Location(ip)
			countryName = dbip['countryName']
			city = dbip['city']

		# 只統計在台灣的IP
		if countryName != "Taiwan":
			continue
		
		result['map'].setdefault(countryName, {})
		result['map'][countryName].setdefault(city, dict(
			positive=0,
			negative=0,
			attendee=0
		))

		if score > 0:
			result['map'][countryName][city]['positive'] += score
		else:
			result['map'][countryName][city]['negative'] += score
		result['map'][countryName][city]['attendee'] += 1
	return result
def getIP2Location(ip):
	ip_split = ip.split(".")
	# IP2Location計算IP的方式,詳細https://www.ip2location.com/docs/db3-ip-country-region-city-specification.pdf
	ip_split = int(ip_split[0])*(256*256*256) + int(ip_split[1])*(256*256) + int(ip_split[2])*256 + int(ip_split[3])
	# 判斷此IP的所縣市
	ipresult = Ip2location.objects.filter(ip_from__lte = ip_split).get(ip_to__gte=ip_split)

	dbip = {}
	dbip['ip'] = ip
	dbip['countryName'] = ipresult.countryName.split(",")[0]
	dbip['city'] = ipresult.city
	dbip['stateProv'] = "unknown"
	dbip['continentName'] = 'unknown'
	
	# 將IP資訊存入mysql,下次遇到同一個IP就可直接讀取
	ipObj, created = IP.objects.update_or_create(
		ip = ip,
		defaults = dbip
	)
	return dbip