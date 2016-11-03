from django.shortcuts import get_object_or_404, render_to_response, render
from django.utils import timezone # auto generate create time.
from django.http import JsonResponse, Http404
from PTT_KCM_API.api.pttJson import pttJson
from functools import wraps
import json, re, os

def queryString_required(str):
	"""	An decorator checking whether queryString key is valid or not
    Args:
        str: allowed queryString key

    Returns:
        if contains invalid queryString key, it will raise exception.
    """
	def _dec(function):
	    @wraps(function)
	    def _wrap(request, *args, **kwargs):
	        if str not in request.GET or request.GET[str] == '':
	        	raise Http404("api does not exist")
	        return function(request, *args, **kwargs)
	    return _wrap
	return _dec

@queryString_required('issue')
def articles(request):
	"""Generate list of term data source files
    Returns:
        if contains invalid queryString key, it will raise exception.
    """
	p = pttJson()
	issue = request.GET['issue']
	if p.hasFile(issue, 'articles'):
		p.articleLists = p.loadFile(p.getIssueFilePath(issue, 'articles'))
	elif os.path.exists(p.getIssueFolderPath(issue)):
		p.fileter_with_issue(issue, 'articles')
		p.saveFile(issue, 'articles', p.articleLists)
	else:
		p.fileter_with_issue(issue, 'articles')
		os.makedirs(p.getIssueFolderPath(issue))
		p.saveFile(issue, 'articles', p.articleLists)
	return JsonResponse(p.get_articles(), safe=False)

