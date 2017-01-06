from django.http import JsonResponse, Http404
from django.urls import reverse
from djangoApiDec.djangoApiDec import queryString_required, date_proc, getJsonFromApi
from PTT_KCM_API.models import IpTable
from PTT_KCM_API.view.pttJson import pttJson
from functools import wraps
from datetime import datetime, date
from collections import OrderedDict

import jieba.posseg as pseg
import jieba.analyse

@date_proc
@queryString_required(['issue'])
def tfidf(request, datetime):
	jieba.analyse.set_stop_words("PTT_KCM_API/view/dictionary/stop_words.txt")
	jieba.analyse.set_idf_path("PTT_KCM_API/view/dictionary/idf.txt.big")
	jieba.load_userdict('PTT_KCM_API/view/dictionary/dict.txt.big.txt')
	jieba.load_userdict('PTT_KCM_API/view/dictionary/jieba_expandDict.txt')
	"""Generate JSON has key TF-IDF value of specific issue.

	Returns:
		{
		  "issue": "馬英九",
		  "totalDocs":150000,
		  "df":{
		  	'馬皇':5000,
		  },
		  "idf":{
		  	'馬皇':log(totalDocs/df),
		  },
		  "articleList":[
		  	{
		  		"articleID":"id1"
		  		"tf":{
		  			"馬皇":1,
		  			'馬娘娘':2
		  		},
		  		'tf-idf':{
					"馬皇":1,
					'馬娘娘':2  			
		  		}
		  	}
		  ]
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
	if p.hasFile(issue, "tfidf", datetime):
		result = p.getFromDB(issue, 'tfidf', datetime)
	else:
		jsonText = getJsonFromApi(request, 'http', 'PTT_KCM_API', 'articles', (('issue', issue),("date", datetime.date())))
		result = dict(
			issue=issue,
			df={},
			articleList=[]
		)
		for article in jsonText:
			# content = pseg.cut(i['content'])
			# messages = ( pseg.cut(['push_content']) for j in i['messages'])
			# tf = set( i for i in content if i[0] in ['nr','n','x'] )
			tags = dict(jieba.analyse.extract_tags(article['content'], topK=10, withWeight=True))
			newtags  = {}
			for i in tags:
				if '.' not in i:
					newtags[i] = tags[i]

			for push in article['messages']:
				pushtags = dict(jieba.analyse.extract_tags(push['push_content'], topK=10, withWeight=True))
				for i in pushtags:
					if i in newtags and '.' not in i:
						newtags[i] = (newtags[i]+pushtags[i])/2
					elif '.' not in i:
						newtags[i] = pushtags[i]
			newtags = OrderedDict(sorted(newtags.items(), key=lambda x:x[1], reverse=True)[:10])

			result['articleList'].append(
				dict(
					articleID=article['article_id'],
					tfidf=newtags
				)
			)

		p.save2DB(issue, 'tfidf', result, datetime)
	return JsonResponse(result, safe=False)