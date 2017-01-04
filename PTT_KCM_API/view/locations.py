from django.http import JsonResponse, Http404
from django.urls import reverse
from functools import wraps
from djangoApiDec.djangoApiDec import queryString_required, date_proc, getJsonFromApi
from PTT_KCM_API.dbip_apiKey import apiKey
from PTT_KCM_API.models import IP
from PTT_KCM_API.view.pttJson import pttJson
from project.settings_database import uri
import json, requests, urllib
from datetime import datetime, date


@date_proc
@queryString_required(['issue'])
def locations(request, datetime):
	""" Generate JSON with location. and score
	Returns:
		{
		  "issue": "大巨蛋",
		  "map": {
		    "Taiwan": {
		      "Taipei City": {
		        "positive": 2.75,
		        "attendee": 3,
		        "negative": 0
		      }
		    }
		  }
		}

	function:
		reverse: reverse will render url pattern, eg: /url/pattern.
		request.get_host: return CNAME + domain name, eg: www.google.com/.
		urllib.parse.quote: change Non-ascii Char into utf-8 Char with %, eg: %E5%85.

	variable:
		urlPattern: pattern of api.
		apiURL: full api url without http protocol.
		jsonText: json response getten from api.
		result:
			issue: the topic you want to query.
			map: data classified by geographic location.
				score: the sentiment value caculated from social network.
  	"""
	issue = request.GET['issue']
	p = pttJson(uri=uri)
	if p.hasFile(issue, "locations", datetime):
		result = p.getFromDB(issue, 'locations', datetime)
	else:
		jsonText = getJsonFromApi(request, 'http', 'PTT_KCM_API', 'ip', (('issue', issue),( "date", datetime.date())))
		result = dict(
			map={}
		)

		ipList = set( (i['ip'], i['score'])
			for i in jsonText['attendee']
				if i['ip'] != None and i['ip'] != "None"
		)
		ipList = ipList.union(set( (i['ip'], i['score'])
			for i in jsonText['author']
				if i['ip'] != None and i['ip'] != "None"
		))
		build_map(ipList, result)
		p.save2DB(issue, 'locations', result, datetime)

	return JsonResponse(result, safe=False)

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
			dbip = requests.get('http://api.eurekapi.com/iplocation/v1.8/locateip?key=SAK2469C36HQB53H65RZ&ip=' + ip + '&format=JSON')
			dbip = json.loads(dbip.text)
			countryName = dbip['geolocation_data']['country_name'],
			stateProv = 'Taiwan Province',
			city = dbip['geolocation_data']['city'],
			continentName = dbip['geolocation_data']['continent_name']

		if countryName != "Taiwan":
			continue
		result['map'].setdefault(countryName, {})
		result['map'][countryName].setdefault(stateProv, dict(
			positive=0,
			negative=0,
			attendee=0
		))

		if score > 0:
			result['map'][countryName][stateProv]['positive'] += score
		else:
			result['map'][countryName][stateProv]['negative'] += score
		result['map'][countryName][stateProv]['attendee'] += 1
