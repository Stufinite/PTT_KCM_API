from django.http import JsonResponse, Http404
from django.urls import reverse
from djangoApiDec.djangoApiDec import queryString_required, date_proc, getJsonFromApi
from PTT_KCM_API.models import IpTable
from PTT_KCM_API.api.pttJson import pttJson
from functools import wraps
from datetime import datetime, date
import jieba.posseg as pseg
import jieba.analyse
from collections import OrderedDict

@date_proc
@queryString_required(['issue'])
def tfidf(request, date):
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
	if p.hasFile(issue, "tfidf", date):
		result = p.loadFile(p.getIssueFilePath(issue, 'tfidf', date))
	else:
		jsonText = getJsonFromApi(request, 'http', 'PTT_KCM_API', 'articles', (('issue', issue)))
		jieba.analyse.set_stop_words("PTT_KCM_API/api/dictionary/stop_words.txt")
		jieba.analyse.set_idf_path("PTT_KCM_API/api/dictionary/idf.txt.big")
		jieba.load_userdict('PTT_KCM_API/api/dictionary/dict.txt.big.txt')
		jieba.load_userdict('PTT_KCM_API/api/dictionary/jieba_expandDict.txt')

		result = dict(
			issue=issue,
			totalDocs=p.length,
			df={},
			articleList=[]
		)
		for article in jsonText:
			# content = pseg.cut(i['content'])
			# messages = ( pseg.cut(['push_content']) for j in i['messages'])
			# tf = set( i for i in content if i[0] in ['nr','n','x'] )
			tags = dict(jieba.analyse.extract_tags(article['content'], topK=10, withWeight=True))
			for push in article['messages']:
				pushtags = dict(jieba.analyse.extract_tags(push['push_content'], topK=10, withWeight=True))
				for i in pushtags:
					if i in tags:
						tags[i] = (tags[i]+pushtags[i])/2
					else:
						tags[i] = pushtags[i]
			# tags = sorted(tags, key=lambda x:x[1])
			# tags[:10]
			########
			tags = OrderedDict(sorted(tags.items(), key=lambda x:x[1], reverse=True)[:10])
			#######
			result['articleList'].append(
				dict(
					articleID=article['article_id'],
					tfidf=tags
				)
			)

		p.saveFile(issue, 'tfidf', result, date)
	return JsonResponse(result, safe=False)