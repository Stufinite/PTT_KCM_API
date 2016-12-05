from django.http import JsonResponse, Http404
from django.urls import reverse
from functools import wraps
from djangoApiDec.djangoApiDec import queryString_required, date_proc, getJsonFromApi
from PTT_KCM_API.dbip_apiKey import apiKey
from PTT_KCM_API.models import IP
from PTT_KCM_API.api.pttJson import pttJson
import json, requests, urllib
from datetime import datetime, date

@date_proc
@queryString_required(['issue'])
def locations(request, date):
	""" Generate JSON with location. and score
	Returns:
		{
		  "issue": "大巨蛋",
		  "map": {
		    "Taiwan": {
		      "Taiwan": {
		        "Fenjihu": {
		          "score": 0, //  分數
		          "attendee": 3 // 參與評論人數
		        },
		        "Fen-chi-hu": {
		          "score": 0,
		          "attendee": 1
		        }
		      },
		      "Taichung City": {
		        "Zhongkeng Village": {
		          "score": 1.0,
		          "attendee": 1
		        }
		      }
		    }
		  },
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
	p = pttJson()
	if p.hasFile(issue, "locations", date):
		result = p.loadFile(p.getIssueFilePath(issue, 'locations', date))
	else:
		jsonText = getJsonFromApi(request, 'http', 'PTT_KCM_API', 'ip', (('issue', issue, "date", date)))
		
		result = dict(
			issue=issue,
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
		p.saveFile(issue, 'locations', result, date)

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
			ipresult = requests.get('http://api.db-ip.com/v2/' + apiKey + '/' + ip)
			ipresult = json.loads(dbip.text)
			countryName = ipresult['countryName']
			stateProv = ipresult['stateProv']
			city = ipresult['city']

		if countryName not in result['map']:
			result['map'][countryName] = {}
		if stateProv not in result['map'][countryName]:
			result['map'][countryName][stateProv] = {}
		if city not in result['map'][countryName][stateProv]:
			result['map'][countryName][stateProv][city] = dict(
				positive=0,
				negative=0,
				attendee=0
			)

		if score > 0:
			result['map'][countryName][stateProv][city]['positive'] += score
		else:
			result['map'][countryName][stateProv][city]['negative'] += score
		result['map'][countryName][stateProv][city]['attendee'] += 1
