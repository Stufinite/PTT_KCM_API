from django.shortcuts import get_object_or_404, render_to_response, render
from django.utils import timezone # auto generate create time.
from django.http import JsonResponse, Http404
from PTT_KCM_API.view.pttJson import pttJson
from functools import wraps
from djangoApiDec.djangoApiDec import queryString_required, date_proc
import json, re, os

@date_proc
@queryString_required(['issue'])
def articles(request, datetime):
	"""Generate list of term data source files
	Returns:
		if contains invalid queryString key, it will raise exception.
	"""
	p = pttJson()
	issue = request.GET['issue']
	return JsonResponse(p.getArticleWithIssue(issue, datetime), safe=False)