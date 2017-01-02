from django.http import JsonResponse, Http404
from django.urls import reverse
from djangoApiDec.djangoApiDec import queryString_required, date_proc, getJsonFromApi
from PTT_KCM_API.models import IpTable
from PTT_KCM_API.view.pttJson import pttJson
from functools import wraps
import json, requests, urllib
from datetime import datetime, date

@date_proc
@queryString_required(['issue'])
def ip(request, datetime):
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
	p = pttJson()
	if p.hasFile(issue, "ip", datetime):
		result = p.getFromDB(issue, 'ip', datetime)
	else:
		jsonText = getJsonFromApi(request, 'http', 'PTT_KCM_API', 'articles', (('issue', issue),("date", datetime.date())))

		result = dict(
			issue=issue, 
			attendee=[], 
			author=[]
		)
		result['author'] = [ dict(
			author=i['author'], 
			ip=get_IpofUser(i['ip'], i['author'].split()[0]) , 
			date=i['date'], 
			score=get_score(i, i['article_title'])) for i in jsonText 
		]
		for i in jsonText:
			for j in i['messages']:
				result['attendee'].append( dict(
						ip=get_IpofUser("", j['push_userid']), 
						push_ipdatetime=j['push_ipdatetime'], 
						push_userid=j['push_userid'], 
						score=get_score(j ,j['push_tag'])) 
				)

		p.save2DB(issue, 'ip', result, datetime)
	return JsonResponse(result, safe=False)

def get_score(obj, text):
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
		try:
			return obj['message_conut']['count']/(obj['message_conut']['push'] + obj['message_conut']['boo'])
		except Exception as e:
			return 0

def get_IpofUser(ip, userID):
	if ip.find('.') != -1:
		return ip
	else:
		ipt = IpTable.objects.filter(userID=userID)
		if len(ipt) == 0:
			return None
		else:
			ipt = ipt[0]
			ipList = ipt.ipList.all()
			return ipList[0].ip