from django.shortcuts import get_object_or_404, render_to_response, render
from django.utils import timezone # auto generate create time.
from django.http import JsonResponse, Http404
from PTT_KCM_API.api.pttJson import pttJson
from functools import wraps
import json, re, os
from datetime import datetime, date

def date_proc(func):
	"""	An decorator checking whether date parameter is passing in or not. If not, default date value is all PTT data.
		Else, return PTT data with right date.
	Args:
		func: function you want to decorate.
		request: WSGI request parameter getten from django.

	Returns:
		date: 
			a datetime variable, you can only give year, year + month or year + month + day, three type.
			The missing part would be assigned default value 1 (for month is Jan, for day is 1).
	"""
	@wraps(func)
	def wrapped(request, *args, **kwargs):
		if 'date' in request.GET and request.GET['date'] == '':
			raise Http404("api does not exist")
		elif 'date' not in request.GET:
			date = datetime.today()
			return func(request, date)
		else:			
			date = tuple(int(intValue) for intValue in request.GET['date'].split('-'))
			if len(date) == 3:
				date = datetime(*date)
			elif len(date) == 2:
				date = datetime(*date, 1)
			else:
				date = datetime(*date, 1, 1)
			return func(request, date)
	return wrapped

def queryString_required(strList):
	"""	An decorator checking whether queryString key is valid or not
	Args:
		str: allowed queryString key

	Returns:
		if contains invalid queryString key, it will raise exception.
	"""
	def _dec(function):
		@wraps(function)
		def _wrap(request, *args, **kwargs):
			for i in strList:
				if i not in request.GET:
					raise Http404("api does not exist")
			return function(request, *args, **kwargs)
		return _wrap
	return _dec

@date_proc
@queryString_required(['issue'])
def articles(request, date):
	"""Generate list of term data source files
	Returns:
		if contains invalid queryString key, it will raise exception.
	"""
	p = pttJson()
	issue = request.GET['issue']

	if p.hasFile(issue, 'articles', date):
		p.articleLists = p.loadFile(p.getIssueFilePath(issue, 'articles', date))
	elif os.path.exists(p.getIssueFolderPath(issue)):
		p.fileter_with_issue(issue, date, 'articles')
		p.saveFile(issue, 'articles', p.articleLists, date)
	else:
		p.fileter_with_issue(issue, date, 'articles')
		os.makedirs(p.getIssueFolderPath(issue))
		p.saveFile(issue, 'articles', p.articleLists, date)
	return JsonResponse(p.get_articles(), safe=False)