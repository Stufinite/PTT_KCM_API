from django.http import JsonResponse, Http404
from django.urls import reverse
from functools import wraps
from PTT_KCM_API.api.articles import queryString_required
import json, requests, urllib

@queryString_required('issue')
def locations(request):
	""" Generate JSON with location. and score
	Returns:
		{
		  "issue": "大巨蛋",
		  "map": [
			{
			  "attendee": 100, // 參與評論人數
			  "location": "台中",
			  "score": 5//  分數
			},
			{
			  "attendee": 63, // 參與評論人數
			  "location": "台南",
			  "score": -3//  分數
			},
		  ]
		}
	
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
			result = build_map(i, result)

	for i in jsonText['author']:
		if i['ip'] != None and i['ip'] != "None":
			result = build_map(i, result)
			
	return JsonResponse(result, safe=False)

def build_map(i, result):
	url = 'http://api.db-ip.com/v2/9f7517a1398793441adf0ffe53885933e42a92fe/' + i['ip']
	dbip = requests.get(url)
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
	return result