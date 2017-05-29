from django.http import JsonResponse, Http404
from django.urls import reverse
from djangoApiDec.djangoApiDec import queryString_required, date_proc, getJsonFromApi
from PTT_KCM_API.models import IpTable
from PTT_KCM_API.view.pttJson import pttJson
from functools import wraps
import json, requests, urllib
from datetime import datetime, date
from Swinger import Swinger
from .articles import articles

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
		jsonText = getJsonFromApi(articles, request)

		result = dict(
			issue=issue, 
			attendee=[], 
			author=[]
		)
		s = Swinger()
		s.load('LogisticRegression') # 或是其他模型例如MultinomialNB

		result['author'] = [ dict(
			author=i['author'], 
			ip=get_IpofUser(i['ip'], i['author'].split()[0]) , 
			date=i['date'], 
			score=1 if s.swing(i['content'])=='pos' else -1) 
			for i in jsonText 
				if i['author'] != None and i['author'] != "None"
		]
		
		for i in jsonText:
			for j in i['messages']:
				result['attendee'].append( dict(
						ip=get_IpofUser("", j['push_userid']), 
						push_ipdatetime=j['push_ipdatetime'], 
						push_userid=j['push_userid'], 
						score=1 if s.swing(j['push_content'])=='pos' else -1) 
				)

		# p.save2DB(issue, 'ip', result, datetime)
	return JsonResponse(result, safe=False)

def get_IpofUser(ip, userID):
	if ip.find('.') != -1:
		return ip
	else:
		try:
			ipt = IpTable.objects.filter(userID=userID)
			if len(ipt) == 0:
				return None
			else:
				ipt = ipt[0]
				ipList = ipt.ipList.all()
				return ipList[0].ip
		except Exception as e:
			print(e)
			print("error")