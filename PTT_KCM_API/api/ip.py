from django.http import JsonResponse, Http404
from django.urls import reverse
from PTT_KCM_API.api.articles import queryString_required
from functools import wraps
import json, requests, urllib

@queryString_required('issue')
def ip(request):
	"""Generate JSON has key of Issue, attendee, author.

	Returns:
		{
		  "attendee": [ # ptt留言
			{
			  "ip": "140.120.4.13",
			  "push_ipdatetime": "10/25 11:34",
			  "push_userid": "McCain",
			  "score": "3"
			}
		  ],
		  "author": { # 發文者
			"ip": "140.120.4.13",
			"push_ipdatetime": "10/25 11:34",
			"push_userid": "McCain",
			"score": "3"
		  },
		  "issue": "大巨蛋"
		}

	function:
		reverse: reverse will render url pattern, eg: /url/pattern.
		request.get_host: return CNAME + domain name, eg: www.google.com/.
		urllib.parse.quote: change Non-ascii Char into utf-8 Char with %, eg: %E5%85.

	variable:
		urlPattern: pattern of api.
		apiURL: full api url without http protocol.
		jsonText: json response getten from api.
	"""
	issue = request.GET['issue']
	urlPattern = reverse('PTT_KCM_API:articles')
	apiURL = request.get_host() + urlPattern +"?issue={}".format(urllib.parse.quote(issue))
	jsonText = requests.get('http://' + apiURL)

	jsonText = json.loads(jsonText.text)
	result = dict(issue=issue, attendee=[], author=[])
	result['author'] = [ dict(author=i['author'], ip=i['ip'], date=i['date'], score=0) for i in jsonText ]
	for i in jsonText:
		for j in i['messages']:
			result['attendee'].append( dict(
					ip=None, 
					push_ipdatetime=j['push_ipdatetime'], 
					push_userid=j['push_userid'], 
					score=get_score(j['push_tag'])) 
			)
	return JsonResponse(result, safe=False)

def get_score(text):
	'''Return the score of attitude toward a specific issue.

	IF block: return score of comment.

	Else block: return score of author.

	'''
	if len(text) == 1:
		if text == "噓":
			return -1
		elif text == "→":
			return 0
		elif text == "推":
			return 1
	else:
		return 0

