from django.http import JsonResponse, Http404
from django.urls import reverse
from functools import wraps
from PTT_KCM_API.api.articles import queryString_required
from PTT_KCM_API.dbip_apiKey import apiKey
import json, requests, urllib

@queryString_required('issue')
def locations(request):
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
	urlPattern = reverse('PTT_KCM_API:ip')
	apiURL = request.get_host() + urlPattern +"?issue={}".format(urllib.parse.quote(issue))
	jsonText = requests.get('http://' + apiURL)
	jsonText = json.loads(jsonText.text)


	result = dict(
		issue=issue,
		map={}
	)
	score = 0
	for i in jsonText['attendee']:
		if i['ip'] != None and i['ip'] != "None":
			build_map(i, result)

	for i in jsonText['author']:
		if i['ip'] != None and i['ip'] != "None":
			build_map(i, result)
			
	return JsonResponse(result, safe=False)

def build_map(i, result):
	''' Create map instance.

	dbip: ip-location json return from dbip api.
	
	if clause: if key name (eq:台南) doesn't exist, then create dict with that key name and calculate score and attendee.
	'''
	dbip = requests.get('http://api.db-ip.com/v2/' + apiKey + '/' + i['ip'])
	dbip = json.loads(dbip.text)
	countryName = dbip['countryName']
	stateProv = dbip['stateProv']
	city = dbip['city']


	if countryName not in result['map']:
		result['map'][countryName] = {}
	if stateProv not in result['map'][countryName]:
		result['map'][countryName][stateProv] = {}
	if city not in result['map'][countryName][stateProv]:
		result['map'][countryName][stateProv][city] = dict(
			score=0,
			attendee=0
		)			
	result['map'][countryName][stateProv][city]['score'] += i['score']
	result['map'][countryName][stateProv][city]['attendee'] += 1