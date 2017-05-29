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

s = Swinger()
s.load('LogisticRegression') # 或是其他模型例如MultinomialNB

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

		result['author'] = [ dict(
			author=i['author'], 
			ip=get_IpofUser(i['ip'], i['author'].split()[0]) , 
			date=i['date'], 
			score=1 if s.swingList(i['content'])=='pos' else -1) 
			for i in jsonText 
				if i['author'] != None and i['author'] != "None"
		]

		# 因為本文是負,True代表要使用負負得正，
		reverseFlag = list(map(lambda x:True if x['score'] == -1 else False, result['author']))
		
		for i, zipflag in zip(jsonText, reverseFlag):
			for j in i['messages']:
				score = 1 if s.swingList(j['push_content'])=='pos' else -1
				if zipflag:
					score *= -1
				result['attendee'].append( dict(
						ip=get_IpofUser("", j['push_userid']), 
						push_ipdatetime=j['push_ipdatetime'], 
						push_userid=j['push_userid'], 
						score=score) 
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