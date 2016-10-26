from django.shortcuts import get_object_or_404, render_to_response, render
from django.utils import timezone # auto generate create time.
from django.http import JsonResponse

import json, re

def ip(request):
	p = pttJson('PTT_KCM_API/api/ptt.json')
	return JsonResponse(p.getWithIssue(p.get_pttJson(),'光復節'), safe=False)

class pttJson(object):
	"""docstring for pttJson"""
	def __init__(self, filePath):
		self.filePath = filePath
		self.get_pttJson()

	def get_pttJson(self):
		with open(self.filePath, 'r', encoding='utf8') as f:
			result = json.load(f)
		return result
	def getWithIssue(self, json, issue):
		for i in json['articles']:
			if issue in i['article_title']:
				return i
			else:
				return {}